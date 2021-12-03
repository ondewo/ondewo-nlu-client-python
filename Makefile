ONDEWO_NLU_API_DIR=ondewo-nlu-api
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/

clean_python_api:
	rm ondewo/nlu/*pb2_grpc.py
	rm ondewo/nlu/*pb2.py
	rm ondewo/nlu/*.pyi
	rm ondewo/qa/*pb2_grpc.py
	rm ondewo/qa/*pb2.py
	rm ondewo/qa/*.pyi
	rm -rf google

generate_all_protos: generate_ondewo_protos generate_google_protos
generate_google_protos:
	# generate google api files
	python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} --python_out=. --mypy_out=. --grpc_python_out=. ${GOOGLE_APIS_DIR}/google/api/annotations.proto
	python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} --python_out=. --mypy_out=. --grpc_python_out=. ${GOOGLE_APIS_DIR}/google/rpc/status.proto
	python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} --python_out=. --mypy_out=. --grpc_python_out=. ${GOOGLE_APIS_DIR}/google/type/latlng.proto
	python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} --python_out=. --mypy_out=. --grpc_python_out=. ${GOOGLE_APIS_DIR}/google/api/http.proto
	python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} --python_out=. --mypy_out=. --grpc_python_out=. ${GOOGLE_APIS_DIR}/google/longrunning/operations.proto

generate_ondewo_protos:
	for f in $$(find ${ONDEWO_PROTOS_DIR} -name '*.proto'); do \
		python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} -I${ONDEWO_NLU_API_DIR} --python_out=. --mypy_out=. --grpc_python_out=. $$f; \
	done

build_zip:
	zip -r ondewo-nlu-client-python.zip examples ondewo LICENSE LICENSE.md requirements.txt README.md setup.cfg setup.py

# Git Submodules targets
git_new_branch_recursively:
	git submodule foreach --recursive "git checkout -b $(shell git rev-parse --abbrev-ref HEAD)"
	git submodule foreach --recursive "git push -u origin $(shell git rev-parse --abbrev-ref HEAD)"

git_checkout_branch_recursively:
	git submodule foreach --recursive "git checkout $(shell git rev-parse --abbrev-ref HEAD)"
	git submodule foreach --recursive "git pull"

git_checkout_develop_recursively:
	git submodule foreach --recursive "git checkout develop"
	git submodule foreach --recursive "git pull"

git_merge_develop_in_recursively: git_checkout_branch_recursively
	git pull
	git pull origin develop
	git submodule foreach --recursive "git pull"
	git submodule foreach --recursive "git pull origin develop"

git_push_recursively:
	git submodule foreach --recursive "git push"
	git push

git_status_recursively:
	git submodule foreach --recursive "git status"
	git submodule status --recursive

push_to_pypi: build_package upload_package clear_package_data
	echo 'pushed to pypi : )'

build_package:
	python setup.py sdist bdist_wheel

upload_package:
	twine upload -r pypi dist/*

clear_package_data:
	rm -rf build dist ondewo_nlu_client.egg-info
