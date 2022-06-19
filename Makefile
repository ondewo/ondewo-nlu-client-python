# Fully automated build and deploy process for ondewo-nlu-client-python
#
# Step 1: Configure bellow the versions for build
# Step 2: Configure your pypi user name and password
# Step 3: Execute "make build_and_push_to_pypi_via_docker"

# Choose the submodule version to build ondewo-nlu-client-python
ONDEWO_NLU_API_GIT_BRANCH=tags/2.8.0
ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/2.0.0
PYPI_USERNAME=
PYPI_PASSWORD=

# Submodule paths
ONDEWO_NLU_API_DIR=ondewo-nlu-api
ONDEWO_PROTO_COMPILER_DIR=ondewo-proto-compiler

# Specify protos directories
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/

# Pypi release docker image environment variables
IMAGE_PYPI_NAME=ondewo-nlu-client-python:latest

# Release automation for building and pushing to pypi via a docker image
build_and_push_to_pypi_via_docker: build build_pypi_docker_image push_to_pypi_via_docker_image

build: clear_package_data init_submodules checkout_defined_submodule_versions build_compiler generate_ondewo_protos

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

checkout_defined_submodule_versions:
	@echo "START checking out submodules ..."
	git -C ${ONDEWO_NLU_API_DIR} fetch --all
	git -C ${ONDEWO_NLU_API_DIR} checkout ${ONDEWO_NLU_API_GIT_BRANCH}
	git -C ${ONDEWO_PROTO_COMPILER_DIR} fetch --all
	git -C ${ONDEWO_PROTO_COMPILER_DIR} checkout ${ONDEWO_PROTO_COMPILER_GIT_BRANCH}
	@echo "DONE checking out submodules"

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

build_pypi_docker_image:
	docker build -f Dockerfile.pypi -t ${IMAGE_PYPI_NAME} .

push_to_pypi_via_docker_image: 
	[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	docker run --rm \
		-v ${shell pwd}/dist:/home/ondewo/dist \
		-e PYPI_USERNAME=${PYPI_USERNAME} \
		-e PYPI_PASSWORD=${PYPI_PASSWORD} \
		${IMAGE_PYPI_NAME} make push_to_pypi

push_to_pypi: build_package upload_package clear_package_data
	echo 'pushed to pypi : )'

build_package:
	python setup.py sdist bdist_wheel

upload_package:
	twine upload --verbose -r pypi dist/* -u${PYPI_USERNAME} -p${PYPI_PASSWORD}

clear_package_data:
	rm -rf build dist ondewo_nlu_client.egg-info
