include ./envs/versions.env
export
export GH_TOKEN=
# Fully automated build and deploy process for ondewo-nlu-client-python
# Release Process Steps:
# 1 - Create Release Branch and push
# 2 - Create Release Tag and push
# 2 - GitHub Release
# 3 - PyPI Release

CURRENT_RELEASE_NOTES=`cat RELEASE.md \
	| sed -n '/Release ONDEWO NLU Python Client ${ONDEWO_NLU_VERSION}/,/\*\*/p'`

# Choose repo to release to - Example: "https://github.com/ondewo/ondewo-nlu-client-python"
GH_REPO="https://github.com/ondewo/ondewo-nlu-client-python"

# Submodule paths
ONDEWO_NLU_API_DIR=ondewo-nlu-api
ONDEWO_PROTO_COMPILER_DIR=ondewo-proto-compiler

# Specify protos directories
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/
OUTPUT_DIR=.

# Utils release docker image environment variables
IMAGE_UTILS_NAME=ondewo-nlu-client-utils-python:${ONDEWO_NLU_VERSION}

.DEFAULT_GOAL := help

# First comment after target starting with double ## specifies usage
help:  ## Print usage info about help targets
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' Makefile | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

# BEFORE "release"
update_setup: ## Update NLU Version in setup.py
	@sed -i "s/version='[0-9]*.[0-9]*.[0-9]*'/version='${ONDEWO_NLU_VERSION}'/g" setup.py


release: ## Automate the entire release process
	@echo "Release Automation started"
	create_release_branch
	create_release_tag
	build_and_release_to_github_via_docker
	build_and_push_to_pypi_via_docker
	@echo "Release Finished"

create_release_branch: ## Create Release Branch and push it to origin
	git checkout -b "release/${ONDEWO_NLU_VERSION}"
	git push -u origin "release/${ONDEWO_NLU_VERSION}"

create_release_tag: ## Create Release Tag and push it to origin
	git tag -a ${ONDEWO_NLU_VERSION} -m "release/${ONDEWO_NLU_VERSION}"
	git push origin ${ONDEWO_NLU_VERSION}

build_and_push_to_pypi_via_docker: build build_utils_docker_image push_to_pypi_via_docker_image  ## Release automation for building and pushing to pypi via a docker image

build_and_release_to_github_via_docker: build build_utils_docker_image release_to_github_via_docker_image  ## Release automation for building and releasing on GitHub via a docker image

login_to_gh: ## Login to Github CLI with Access Token
	echo $(GITHUB_GH_TOKEN) | gh auth login -p ssh --with-token

build_gh_release: ## Generate Github Release with CLI
	gh release create --repo $(GH_REPO) "$(ONDEWO_NLU_VERSION)" -n "$(CURRENT_RELEASE_NOTES)" -t "Release ${ONDEWO_NLU_VERSION}"

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

push_to_gh: login_to_gh build_gh_release
	@echo 'Released to Github'

release_to_github_via_docker_image:  ## Release to Github via docker
	docker run --rm \
		${IMAGE_UTILS_NAME} make push_to_gh


build_package:
	python setup.py sdist bdist_wheel
	chmod a+rw dist -R

upload_package:
	twine upload --verbose -r pypi dist/* -u${PYPI_USERNAME} -p${PYPI_PASSWORD}

clear_package_data:
	rm -rf build dist/* ondewo_nlu_client.egg-info

