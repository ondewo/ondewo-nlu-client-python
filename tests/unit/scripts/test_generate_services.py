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
import textwrap
from pathlib import Path

import pytest

from ondewo.nlu.scripts.generate_services import (
    RpcMethod,
    ServiceDef,
    _build_file_content,
    camel_to_snake,
    main,
    parse_proto_file,
    proto_stem_to_file_name,
    resolve_type,
)


# ---------------------------------------------------------------------------
# camel_to_snake
# ---------------------------------------------------------------------------

class TestCamelToSnake:
    def test_simple_pascal(self) -> None:
        assert camel_to_snake('Rags') == 'rags'

    def test_two_words(self) -> None:
        assert camel_to_snake('EntityTypes') == 'entity_types'

    def test_three_words(self) -> None:
        assert camel_to_snake('ProjectStatistics') == 'project_statistics'

    def test_rpc_name(self) -> None:
        assert camel_to_snake('RagAsk') == 'rag_ask'

    def test_long_rpc_name(self) -> None:
        assert camel_to_snake('RagConstructKnowledgeGraph') == 'rag_construct_knowledge_graph'

    def test_leading_acronym_no_separator(self) -> None:
        # "AI" is all-uppercase at the start → no underscore inserted before "Services"
        # because there is no lowercase letter before "S"
        assert camel_to_snake('AIServices') == 'aiservices'

    def test_mixed_acronym_separator(self) -> None:
        # 'i' (lowercase) before 'S' → underscore IS inserted
        assert camel_to_snake('AiServices') == 'ai_services'

    def test_ccai_prefix(self) -> None:
        assert camel_to_snake('CcaiProjects') == 'ccai_projects'

    def test_already_snake(self) -> None:
        assert camel_to_snake('rags') == 'rags'


# ---------------------------------------------------------------------------
# proto_stem_to_file_name
# ---------------------------------------------------------------------------

class TestProtoStemToFileName:
    def test_regular_stem_gets_s(self) -> None:
        assert proto_stem_to_file_name('agent') == 'agents'

    def test_rag_gets_s(self) -> None:
        assert proto_stem_to_file_name('rag') == 'rags'

    def test_context_gets_s(self) -> None:
        assert proto_stem_to_file_name('context') == 'contexts'

    def test_entity_type_gets_s(self) -> None:
        assert proto_stem_to_file_name('entity_type') == 'entity_types'

    def test_utility_y_to_ies(self) -> None:
        assert proto_stem_to_file_name('utility') == 'utilities'

    def test_already_ends_in_s_unchanged(self) -> None:
        assert proto_stem_to_file_name('operations') == 'operations'

    def test_already_ends_in_s_aiservices(self) -> None:
        assert proto_stem_to_file_name('aiservices') == 'aiservices'

    def test_server_statistics_unchanged(self) -> None:
        assert proto_stem_to_file_name('server_statistics') == 'server_statistics'


# ---------------------------------------------------------------------------
# resolve_type
# ---------------------------------------------------------------------------

class TestResolveType:
    def test_bare_name_no_import(self) -> None:
        bare, imp = resolve_type('RagAskRequest')
        assert bare == 'RagAskRequest'
        assert imp is None

    def test_google_protobuf_empty(self) -> None:
        bare, imp = resolve_type('google.protobuf.Empty')
        assert bare == 'Empty'
        assert imp == 'from google.protobuf.empty_pb2 import Empty'

    def test_google_protobuf_field_mask(self) -> None:
        bare, imp = resolve_type('google.protobuf.FieldMask')
        assert bare == 'FieldMask'
        assert imp == 'from google.protobuf.field_mask_pb2 import FieldMask'

    def test_google_protobuf_timestamp(self) -> None:
        bare, imp = resolve_type('google.protobuf.Timestamp')
        assert bare == 'Timestamp'
        assert imp == 'from google.protobuf.timestamp_pb2 import Timestamp'

    def test_ondewo_nlu_operation(self) -> None:
        bare, imp = resolve_type('ondewo.nlu.Operation')
        assert bare == 'Operation'
        assert imp == 'from ondewo.nlu.operations_pb2 import Operation'

    def test_ondewo_nlu_unknown_falls_back_to_local(self) -> None:
        bare, imp = resolve_type('ondewo.nlu.SomeUnknownType')
        assert bare == 'SomeUnknownType'
        assert imp is None  # best-effort fallback

    def test_unknown_namespace_strips_prefix(self) -> None:
        bare, imp = resolve_type('foo.bar.Baz')
        assert bare == 'Baz'
        assert imp is None


# ---------------------------------------------------------------------------
# parse_proto_file
# ---------------------------------------------------------------------------

class TestParseProtoFile:
    def _write_proto(self, tmp_path: Path, name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(textwrap.dedent(content))
        return p

    def test_simple_unary_rpc(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (RagAskResponse);
            }
        """)
        services = parse_proto_file(proto)
        assert len(services) == 1
        svc = services[0]
        assert svc.name == 'Rags'
        assert svc.proto_stem == 'rag'
        assert len(svc.rpcs) == 1
        rpc = svc.rpcs[0]
        assert rpc.name == 'RagAsk'
        assert rpc.request_type == 'RagAskRequest'
        assert rpc.response_type == 'RagAskResponse'
        assert not rpc.client_streaming
        assert not rpc.server_streaming

    def test_server_streaming_rpc(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (stream RagAskResponse);
            }
        """)
        rpc = parse_proto_file(proto)[0].rpcs[0]
        assert rpc.server_streaming is True
        assert rpc.client_streaming is False

    def test_client_streaming_rpc(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagUpload (stream RagUploadRequest) returns (RagDocument);
            }
        """)
        rpc = parse_proto_file(proto)[0].rpcs[0]
        assert rpc.client_streaming is True
        assert rpc.server_streaming is False

    def test_multiple_rpcs(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagCreate (RagCreateRequest) returns (RagDataset);
                rpc RagDelete (RagDeleteRequest) returns (RagPartialSuccess);
                rpc RagList   (RagListRequest)   returns (RagDatasetList);
            }
        """)
        rpcs = parse_proto_file(proto)[0].rpcs
        assert [r.name for r in rpcs] == ['RagCreate', 'RagDelete', 'RagList']

    def test_external_type_full_qualified_name_stored(self, tmp_path: Path) -> None:
        # Full qualified names are preserved in RpcMethod so resolve_type can
        # later derive the correct import (e.g. google.protobuf.field_mask_pb2).
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagDelete (RagDatasetIdRequest) returns (google.protobuf.Empty);
                rpc RagStart  (RagStartRequest)     returns (ondewo.nlu.Operation);
            }
        """)
        rpcs = parse_proto_file(proto)[0].rpcs
        assert rpcs[0].response_type == 'google.protobuf.Empty'
        assert rpcs[1].response_type == 'ondewo.nlu.Operation'

    def test_proto_with_no_service_returns_empty(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'common.proto', """
            syntax = "proto3";
            message MyMessage { string value = 1; }
        """)
        assert parse_proto_file(proto) == []

    def test_duplicate_rpc_name_is_skipped(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (RagAskResponse);
                rpc RagAsk (RagAskRequest) returns (RagAskResponse);
            }
        """)
        services = parse_proto_file(proto)
        rpcs = services[0].rpcs
        # Only one method despite the duplicate
        assert len(rpcs) == 1
        assert rpcs[0].name == 'RagAsk'
        # Warning emitted to stderr
        captured = capsys.readouterr()
        assert 'duplicate' in captured.err.lower()
        assert 'RagAsk' in captured.err

    def test_multiple_services_in_one_proto(self, tmp_path: Path) -> None:
        proto = self._write_proto(tmp_path, 'multi.proto', """
            syntax = "proto3";
            service ServiceA {
                rpc MethodA (RequestA) returns (ResponseA);
            }
            service ServiceB {
                rpc MethodB (RequestB) returns (ResponseB);
            }
        """)
        services = parse_proto_file(proto)
        assert len(services) == 2
        assert services[0].name == 'ServiceA'
        assert services[1].name == 'ServiceB'

    def test_service_body_with_nested_braces(self, tmp_path: Path) -> None:
        # option blocks contain braces and must not confuse the brace counter
        proto = self._write_proto(tmp_path, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (RagAskResponse) {
                    option (google.api.http) = { get: "/v1/rag:ask" };
                }
            }
        """)
        services = parse_proto_file(proto)
        assert len(services) == 1
        assert services[0].rpcs[0].name == 'RagAsk'


# ---------------------------------------------------------------------------
# _build_file_content
# ---------------------------------------------------------------------------

class TestBuildFileContent:
    def _make_svc(self, rpcs: list, proto_stem: str = 'rag', name: str = 'Rags') -> ServiceDef:
        return ServiceDef(name=name, rpcs=rpcs, proto_stem=proto_stem)

    def test_unary_method_signature(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagAsk', 'RagAskRequest', 'RagAskResponse', False, False),
        ])
        content = _build_file_content(svc)
        assert 'def rag_ask(self, request: RagAskRequest) -> RagAskResponse:' in content

    def test_server_streaming_uses_iterator_return(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagStream', 'RagStreamRequest', 'RagStreamResponse', False, True),
        ])
        content = _build_file_content(svc)
        assert 'def rag_stream(self, request: RagStreamRequest) -> Iterator[RagStreamResponse]:' in content
        assert 'from typing import Iterator' in content

    def test_client_streaming_uses_iterator_param(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagUpload', 'RagUploadRequest', 'RagDocument', True, False),
        ])
        content = _build_file_content(svc)
        assert 'def rag_upload(self, request: Iterator[RagUploadRequest]) -> RagDocument:' in content
        assert 'from typing import Iterator' in content

    def test_empty_response_import(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagDelete', 'RagDeleteRequest', 'google.protobuf.Empty', False, False),
        ])
        content = _build_file_content(svc)
        assert 'from google.protobuf.empty_pb2 import Empty' in content
        # Empty must NOT appear in the pb2 import block
        assert 'Empty,' not in content.split('from ondewo.nlu.rag_pb2 import')[1].split(')')[0]

    def test_field_mask_response_import(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagGet', 'RagGetRequest', 'google.protobuf.FieldMask', False, False),
        ])
        content = _build_file_content(svc)
        assert 'from google.protobuf.field_mask_pb2 import FieldMask' in content
        assert 'FieldMask,' not in content.split('from ondewo.nlu.rag_pb2 import')[1].split(')')[0]

    def test_operation_response_import(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagStart', 'RagStartRequest', 'ondewo.nlu.Operation', False, False),
        ])
        content = _build_file_content(svc)
        assert 'from ondewo.nlu.operations_pb2 import Operation' in content
        assert 'Operation,' not in content.split('from ondewo.nlu.rag_pb2 import')[1].split(')')[0]

    def test_no_duplicate_methods(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagAsk', 'RagAskRequest', 'RagAskResponse', False, False),
            RpcMethod('RagList', 'RagListRequest', 'RagListResponse', False, False),
            RpcMethod('RagCreate', 'RagCreateRequest', 'RagDataset', False, False),
        ])
        content = _build_file_content(svc)
        method_lines = [line for line in content.splitlines() if line.strip().startswith('def ') and 'stub' not in line]
        names = [line.split('def ')[1].split('(')[0] for line in method_lines]
        assert len(names) == len(set(names)), f'Duplicate method names found: {names}'

    def test_pb2_types_sorted_and_deduplicated(self) -> None:
        # Two RPCs that share a response type; should appear only once in import block
        svc = self._make_svc([
            RpcMethod('RagCreate', 'RagCreateRequest', 'RagDataset', False, False),
            RpcMethod('RagUpdate', 'RagUpdateRequest', 'RagDataset', False, False),
        ])
        content = _build_file_content(svc)
        pb2_block = content.split('from ondewo.nlu.rag_pb2 import')[1].split(')')[0]
        assert pb2_block.count('RagDataset') == 1

    def test_stub_property_present(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagAsk', 'RagAskRequest', 'RagAskResponse', False, False),
        ])
        content = _build_file_content(svc)
        assert 'def stub(self) -> RagsStub:' in content
        assert 'RagsStub(channel=self.grpc_channel)' in content

    def test_class_name_and_docstring(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagAsk', 'RagAskRequest', 'RagAskResponse', False, False),
        ])
        content = _build_file_content(svc)
        assert 'class Rags(ServicesInterface):' in content
        assert 'See rag.proto.' in content

    def test_stub_call_uses_rpc_pascal_name(self) -> None:
        svc = self._make_svc([RpcMethod('RagConstructKnowledgeGraph', 'RagDatasetIdRequest',
                             'RagConstructKnowledgeGraphResponse', False, False), ])
        content = _build_file_content(svc)
        assert 'self.stub.RagConstructKnowledgeGraph(request' in content

    def test_no_iterator_import_when_not_streaming(self) -> None:
        svc = self._make_svc([
            RpcMethod('RagAsk', 'RagAskRequest', 'RagAskResponse', False, False),
        ])
        content = _build_file_content(svc)
        assert 'from typing import Iterator' not in content


# ---------------------------------------------------------------------------
# main (integration)
# ---------------------------------------------------------------------------

class TestMain:
    def _write_proto(self, directory: Path, name: str, content: str) -> None:
        (directory / name).write_text(textwrap.dedent(content))

    def test_creates_output_directory(self, tmp_path: Path) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services' / 'nested'
        self._write_proto(proto_dir, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (RagAskResponse);
            }
        """)
        main(proto_dir, output_dir)
        assert output_dir.is_dir()

    def test_generates_file_per_service(self, tmp_path: Path) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services'
        self._write_proto(proto_dir, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk (RagAskRequest) returns (RagAskResponse);
            }
        """)
        self._write_proto(proto_dir, 'agent.proto', """
            syntax = "proto3";
            service Agents {
                rpc CreateAgent (CreateAgentRequest) returns (Agent);
            }
        """)
        main(proto_dir, output_dir)
        assert (output_dir / 'rags.py').exists()
        assert (output_dir / 'agents.py').exists()

    def test_generated_file_content_is_valid_python(self, tmp_path: Path) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services'
        self._write_proto(proto_dir, 'rag.proto', """
            syntax = "proto3";
            service Rags {
                rpc RagAsk  (RagAskRequest)           returns (stream RagAskResponse);
                rpc RagStop (RagStopRequest)           returns (google.protobuf.Empty);
                rpc RagUpload (stream RagUploadRequest) returns (RagDocument);
            }
        """)
        main(proto_dir, output_dir)
        content = (output_dir / 'rags.py').read_text()
        # Must compile without SyntaxError
        compile(content, 'rags.py', 'exec')

    def test_proto_without_service_produces_no_file(self, tmp_path: Path) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services'
        self._write_proto(proto_dir, 'common.proto', """
            syntax = "proto3";
            message Foo { string bar = 1; }
        """)
        main(proto_dir, output_dir)
        assert list(output_dir.glob('*.py')) == []

    def test_output_collision_emits_warning(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services'
        # 'rag.proto'  -> rags.py  (rag + s)
        # 'rags.proto' -> rags.py  (already ends in s, unchanged)
        self._write_proto(proto_dir, 'rag.proto', """
            syntax = "proto3";
            service Rags { rpc RagAsk (RagAskRequest) returns (RagAskResponse); }
        """)
        self._write_proto(proto_dir, 'rags.proto', """
            syntax = "proto3";
            service Rags { rpc RagList (RagListRequest) returns (RagListResponse); }
        """)
        main(proto_dir, output_dir)
        captured = capsys.readouterr()
        assert 'WARNING' in captured.err
        assert 'rags.py' in captured.err

    def test_utility_pluralised_to_utilities(self, tmp_path: Path) -> None:
        proto_dir = tmp_path / 'protos'
        proto_dir.mkdir()
        output_dir = tmp_path / 'services'
        self._write_proto(proto_dir, 'utility.proto', """
            syntax = "proto3";
            service Utilities {
                rpc ValidateFoo (ValidateFooRequest) returns (ValidateFooResponse);
            }
        """)
        main(proto_dir, output_dir)
        assert (output_dir / 'utilities.py').exists()
        assert not (output_dir / 'utilitys.py').exists()
