ONDEWO_NLU_API_DIR=ondewo-nlu-api
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/

NLU_API_GIT_BRANCH=tags/2.6.0
NLU_APIS_DIR=ondewo-nlu-api
NLU_PROTOS_DIR=${NLU_APIS_DIR}/ondewo
GOOGLE_APIS_DIR=${NLU_APIS_DIR}/googleapis
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google

clean_python_api:
	rm ondewo/nlu/*pb2_grpc.py
	rm ondewo/nlu/*pb2.py
	rm ondewo/nlu/*.pyi
	rm ondewo/qa/*pb2_grpc.py
	rm ondewo/qa/*pb2.py
	rm ondewo/qa/*.pyi
	rm -rf google

build_compiler:
	make -C ondewo-proto-compiler/python build

generate_ondewo_protos:
	make -f ondewo-proto-compiler/python/Makefile run \
		PROTO_DIR=${ONDEWO_PROTOS_DIR} \
		EXTRA_PROTO_DIR=${GOOGLE_PROTOS_DIR} \
		TARGET_DIR='ondewo' \
		OUTPUT_DIR='.'

build_zip:
	zip -r ondewo-nlu-client-python.zip examples ondewo LICENSE LICENSE.md requirements.txt README.md setup.cfg setup.py

# Git Submodules targets

init_submodules:
	@echo "START initializing submodules ..."
	git submodule update --init --recursive
	@echo "DONE initializing submodules"

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
