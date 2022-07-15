# Fully automated build and deploy process for ondewo-nlu-client-python
#
# Step 1: Configure bellow the versions for build
# Step 2: Configure your pypi user name and password
# Step 3: Execute "make build_and_push_to_pypi_via_docker"
# Step 4 (Github Release): Execute "make build_and_release_to_github_via_docker"

# Specify Github Release Number and Release Notes
CURRENT_RELEASE_TAG=`cat RELEASE.md | grep '2.8' | head -1 | cut -c 37-41`
CURRENT_RELEASE_NOTES=`cat RELEASE.md | grep -A 6 'Release ONDEWO' | head -6`

# Choose the submodule version to build ondewo-nlu-client-python
ONDEWO_NLU_API_GIT_BRANCH=tags/2.8.0
ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/2.0.0
PYPI_USERNAME=ENTER_HERE_YOUR_PYPI_USERNAME
PYPI_PASSWORD=ENTER_HERE_YOUR_PYPI_PASSWORD

# You need to setup an access token at https://github.com/settings/tokens - permissions are important
GH_TOKEN=ENTER_HERE_YOUR_TOKEN

# Choose repo to release to - Example: "https://github.com/ondewo/ondewo-nlu-client-python"
GH_REPO=ENTER_HERE_YOUR_REPO

# Submodule paths
ONDEWO_NLU_API_DIR=ondewo-nlu-api
ONDEWO_PROTO_COMPILER_DIR=ondewo-proto-compiler

# Specify protos directories
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/
OUTPUT_DIR=.

# Utils release docker image environment variables
IMAGE_UTILS_NAME=ondewo-nlu-client-python:latest

.PHONY: help build install

.DEFAULT_GOAL := help

# First comment after target starting with double ## specifies usage
help:  ## Print usage info about help targets
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' Makefile | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

build_and_push_to_pypi_via_docker: build build_utils_docker_image push_to_pypi_via_docker_image  ## Release automation for building and pushing to pypi via a docker image

build_and_release_to_github_via_docker: build build_utils_docker_image release_to_github_via_docker_image  ## Release automation for building and releasing on GitHub via a docker image

login_to_gh: ## Login to Github CLI with Access Token
	echo $(GH_TOKEN) | gh auth login -p ssh --with-token

build_gh_release: ## Generate Github Release with CLI
	gh release create --repo "$(GH_REPO)" "$(CURRENT_RELEASE_TAG)" -n "$(CURRENT_RELEASE_NOTES)" -t "Release ${"$(CURRENT_RELEASE_TAG)"}"

build: clear_package_data init_submodules checkout_defined_submodule_versions build_compiler generate_ondewo_protos  ## Build source code

install:  ## Install requirements
	pip install .
	pip install -r requirements.txt

clean_python_api:  ## Clear generated python files
	rm ondewo/nlu/*pb2_grpc.py
	rm ondewo/nlu/*pb2.py
	rm ondewo/nlu/*.pyi
	rm ondewo/qa/*pb2_grpc.py
	rm ondewo/qa/*pb2.py
	rm ondewo/qa/*.pyi
	rm -rf google

build_compiler:  ## Build proto compiler docker image
	make -C ondewo-proto-compiler/python build

generate_ondewo_protos:  ## Generate python code from proto files
	make -f ondewo-proto-compiler/python/Makefile run \
		PROTO_DIR=${ONDEWO_PROTOS_DIR} \
		EXTRA_PROTO_DIR=${GOOGLE_PROTOS_DIR} \
		TARGET_DIR='ondewo' \
		OUTPUT_DIR=${OUTPUT_DIR}

init_submodules:  ## Initialize submodules
	@echo "START initializing submodules ..."
	git submodule update --init --recursive
	@echo "DONE initializing submodules"

checkout_defined_submodule_versions:  ## Update submodule versions
	@echo "START checking out submodules ..."
	git -C ${ONDEWO_NLU_API_DIR} fetch --all
	git -C ${ONDEWO_NLU_API_DIR} checkout ${ONDEWO_NLU_API_GIT_BRANCH}
	git -C ${ONDEWO_PROTO_COMPILER_DIR} fetch --all
	git -C ${ONDEWO_PROTO_COMPILER_DIR} checkout ${ONDEWO_PROTO_COMPILER_GIT_BRANCH}
	@echo "DONE checking out submodules"

build_utils_docker_image:  ## Build utils docker image
	docker build -f Dockerfile.utils -t ${IMAGE_UTILS_NAME} .

push_to_pypi_via_docker_image:  ## Push source code to pypi via docker
	[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	docker run --rm \
		-v ${shell pwd}/dist:/home/ondewo/dist \
		-e PYPI_USERNAME=${PYPI_USERNAME} \
		-e PYPI_PASSWORD=${PYPI_PASSWORD} \
		${IMAGE_UTILS_NAME} make push_to_pypi
	rm -rf dist

push_to_pypi: build_package upload_package clear_package_data
	@echo 'YAY - Pushed to pypi : )'

release_to_github_via_docker_image:  ## Release to Github via docker
	docker run --rm \
		${IMAGE_UTILS_NAME} make login_to_gh build_gh_release


build_package:
	python setup.py sdist bdist_wheel 
	chmod a+rw dist -R

upload_package:
	twine upload --verbose -r pypi dist/* -u${PYPI_USERNAME} -p${PYPI_PASSWORD}

clear_package_data:
	rm -rf build dist/* ondewo_nlu_client.egg-info

