#!/usr/bin/env python3
# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generate service wrapper Python files from proto service definitions.

Usage:
    python3 generate_services.py <proto_dir> <output_dir>

Example:
    python3 ondewo/nlu/scripts/generate_services.py \\
        ondewo-nlu-api/ondewo/nlu \\
        ondewo/nlu/services
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

_COPYRIGHT = """\
# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.\
"""

# Explicit import overrides for ondewo.nlu.* types that live in a different
# pb2 module than the service being generated.
_ONDEWO_NLU_IMPORTS: Dict[str, str] = {
    'Operation': 'from ondewo.nlu.operations_pb2 import Operation',
}


@dataclass
class RpcMethod:
    name: str
    request_type: str   # full qualified proto name, e.g. "google.protobuf.Empty" or "RagAskRequest"
    response_type: str  # full qualified proto name
    client_streaming: bool
    server_streaming: bool


@dataclass
class ServiceDef:
    name: str        # as written in proto, e.g. "Rags"
    rpcs: List[RpcMethod]
    proto_stem: str  # proto filename without extension, e.g. "rag"


def camel_to_snake(name: str) -> str:
    """CamelCase → snake_case.

    Inserts an underscore only where a lowercase letter (or digit) is
    immediately followed by an uppercase letter, so acronyms at the start of a
    name are preserved as a single word:
      RagAsk        -> rag_ask
      AiServices    -> ai_services  (i before S triggers insertion)
      AIServices    -> aiservices   (no lowercase before any uppercase run)
    """
    return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', name).lower()


def proto_stem_to_file_name(stem: str) -> str:
    """Derive the Python service file name (without .py) from the proto stem.

    Mirrors the naming convention used in this project:
      agent            -> agents
      utility          -> utilities   (y -> ies)
      operations       -> operations  (already ends in s)
      aiservices       -> aiservices  (already ends in s)
    """
    if stem.endswith('y'):
        return stem[:-1] + 'ies'
    if stem.endswith('s'):
        return stem
    return stem + 's'


def resolve_type(qualified: str) -> Tuple[str, Optional[str]]:
    """Resolve a proto type name to a (bare_name, import_line_or_None) pair.

    Rules:
    - Bare name (no dot): local type — import from the service's own _pb2.
    - google.protobuf.*: derive the pb2 module name from the type name via
      camel_to_snake, covering the entire namespace generically
      (Empty, FieldMask, Timestamp, Duration, Any, …).
    - ondewo.nlu.*: look up in _ONDEWO_NLU_IMPORTS; unknown types fall back
      to local (best-effort — add a new entry if needed).
    """
    bare = qualified.split('.')[-1]
    if '.' not in qualified:
        return bare, None

    parts = qualified.split('.')
    if parts[0] == 'google' and parts[1] == 'protobuf':
        module = camel_to_snake(bare)  # FieldMask -> field_mask, Empty -> empty
        return bare, f'from google.protobuf.{module}_pb2 import {bare}'

    if parts[0] == 'ondewo' and parts[1] == 'nlu':
        imp = _ONDEWO_NLU_IMPORTS.get(bare)
        return bare, imp  # None means "treat as local" (best-effort fallback)

    # Unknown namespace — strip prefix and treat as local (best-effort)
    return bare, None


def parse_proto_file(proto_path: Path) -> List[ServiceDef]:
    """Parse a .proto file and return all ServiceDef objects it contains."""
    content = proto_path.read_text()
    proto_stem = proto_path.stem

    rpc_re = re.compile(
        r'rpc\s+(\w+)\s*\(\s*(stream\s+)?([\w.]+)\s*\)\s*returns\s*\(\s*(stream\s+)?([\w.]+)\s*\)',
        re.DOTALL,
    )

    services: List[ServiceDef] = []
    for svc_match in re.finditer(r'service\s+(\w+)\s*\{', content):
        service_name = svc_match.group(1)

        # Extract the service body by counting braces
        start = svc_match.end()  # position right after the opening {
        depth = 1
        pos = start
        while pos < len(content) and depth > 0:
            if content[pos] == '{':
                depth += 1
            elif content[pos] == '}':
                depth -= 1
            pos += 1
        body = content[start:pos - 1]

        seen_rpc_names: Set[str] = set()
        rpcs: List[RpcMethod] = []
        for r in rpc_re.finditer(body):
            rpc_name = r.group(1)
            if rpc_name in seen_rpc_names:
                print(
                    f'  WARNING: duplicate RPC "{rpc_name}" in service "{service_name}" '
                    f'of {proto_path.name} — skipping duplicate',
                    file=sys.stderr,
                )
                continue
            seen_rpc_names.add(rpc_name)
            rpcs.append(RpcMethod(
                name=rpc_name,
                request_type=r.group(3).strip(),   # keep full qualified name
                response_type=r.group(5).strip(),  # keep full qualified name
                client_streaming=bool(r.group(2)),
                server_streaming=bool(r.group(4)),
            ))

        if rpcs:
            services.append(ServiceDef(name=service_name, rpcs=rpcs, proto_stem=proto_stem))

    return services


def _build_file_content(svc: ServiceDef) -> str:
    """Render a complete Python service wrapper file."""
    needs_iterator = any(r.client_streaming or r.server_streaming for r in svc.rpcs)

    pb2_types: Set[str] = set()
    external_imports: Set[str] = set()
    for rpc in svc.rpcs:
        for qualified in (rpc.request_type, rpc.response_type):
            bare, imp = resolve_type(qualified)
            if imp:
                external_imports.add(imp)
            else:
                pb2_types.add(bare)

    lines: List[str] = [_COPYRIGHT, '']

    if needs_iterator:
        lines += ['from typing import Iterator', '']

    # google.protobuf imports
    google_imports = sorted(i for i in external_imports if i.startswith('from google'))
    if google_imports:
        lines += google_imports + ['']

    # Types from this service's own _pb2 module
    lines.append(f'from ondewo.nlu.{svc.proto_stem}_pb2 import (')
    for t in sorted(pb2_types):
        lines.append(f'    {t},')
    lines.append(')')

    lines.append(f'from ondewo.nlu.{svc.proto_stem}_pb2_grpc import {svc.name}Stub')
    lines.append('from ondewo.nlu.core.services_interface import ServicesInterface')

    # Other external imports (e.g. operations_pb2)
    for imp in sorted(i for i in external_imports if not i.startswith('from google')):
        lines.append(imp)

    lines += [
        '',
        '',
        f'class {svc.name}(ServicesInterface):',
        '    """',
        f'    Exposes the {svc.name}-related endpoints of ONDEWO NLU services in a user-friendly way.',
        '',
        f'    See {svc.proto_stem}.proto.',
        '    """',
        '',
        '    @property',
        f'    def stub(self) -> {svc.name}Stub:',
        f'        stub: {svc.name}Stub = {svc.name}Stub(channel=self.grpc_channel)',
        '        return stub',
    ]

    for rpc in svc.rpcs:
        method = camel_to_snake(rpc.name)
        bare_req, _ = resolve_type(rpc.request_type)
        bare_resp, _ = resolve_type(rpc.response_type)
        req = f'Iterator[{bare_req}]' if rpc.client_streaming else bare_req
        resp = f'Iterator[{bare_resp}]' if rpc.server_streaming else bare_resp
        lines += [
            '',
            f'    def {method}(self, request: {req}) -> {resp}:',
            f'        response: {resp} = self.stub.{rpc.name}(request, metadata=self.metadata)',
            '        return response',
        ]

    lines.append('')
    return '\n'.join(lines)


def main(proto_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    # Track which proto file last wrote each output path so we can warn on collision.
    written_by: Dict[Path, str] = {}
    for proto_path in sorted(proto_dir.glob('*.proto')):
        for svc in parse_proto_file(proto_path):
            file_name = proto_stem_to_file_name(svc.proto_stem)
            out = output_dir / f'{file_name}.py'
            if out in written_by:
                print(
                    f'  WARNING: {out.name} already written by {written_by[out]}, '
                    f'overwriting with service "{svc.name}" from {proto_path.name}',
                    file=sys.stderr,
                )
            written_by[out] = proto_path.name
            out.write_text(_build_file_content(svc))
            print(f'  generated {out}')


if __name__ == '__main__':
    _proto_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('ondewo-nlu-api/ondewo/nlu')
    _output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('ondewo/nlu/services')
    main(_proto_dir, _output_dir)
