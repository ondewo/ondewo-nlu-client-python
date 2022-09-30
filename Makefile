export
# ---------------- BEFORE RELEASE ----------------
# 1 - Update Version Number
# 2 - Update RELEASE.md
# -------------- Release Process Steps --------------
# 1 - Get Credentials from devops-accounts repo
# 2 - Create Release Branch and push
# 3 - Create Release Tag and push
# 4 - GitHub Release
# 5 - PyPI Release

########################################################
# 		Variables
########################################################


# MUST BE THE SAME AS API in Mayor and Minor Version Number
# example: API 2.9.0 --> Client 2.9.X
ONDEWO_NLU_VERSION = 3.3.0

ONDEWO_NLU_API_GIT_BRANCH=tags/3.3.0
ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/4.1.1
PYPI_USERNAME?=ENTER_HERE_YOUR_PYPI_USERNAME
PYPI_PASSWORD?=ENTER_HERE_YOUR_PYPI_PASSWORD

# You need to setup an access token at https://github.com/settings/tokens - permissions are important
GITHUB_GH_TOKEN?=ENTER_YOUR_TOKEN_HERE

CURRENT_RELEASE_NOTES=`cat RELEASE.md \
	| sed -n '/Release ONDEWO NLU Python Client ${ONDEWO_NLU_VERSION}/,/\*\*/p'`


GH_REPO="https://github.com/ondewo/ondewo-nlu-client-python"
DEVOPS_ACCOUNT_GIT="ondewo-devops-accounts"
DEVOPS_ACCOUNT_DIR="./${DEVOPS_ACCOUNT_GIT}"
ONDEWO_NLU_API_DIR=ondewo-nlu-api
ONDEWO_PROTO_COMPILER_DIR=ondewo-proto-compiler
GOOGLE_APIS_DIR=${ONDEWO_NLU_API_DIR}/googleapis
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${GOOGLE_APIS_DIR}/google/
OUTPUT_DIR=.
IMAGE_UTILS_NAME=ondewo-nlu-client-utils-python:${ONDEWO_NLU_VERSION}
.DEFAULT_GOAL := help

########################################################
#       ONDEWO Standard Make Targets
########################################################

setup_developer_environment_locally: install_precommit_hooks install_dependencies_locally

install_precommit_hooks: ## Installs pre-commit hooks and sets them up for the ondewo-csi-client repo
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg

precommit_hooks_run_all_files: ## Runs all pre-commit hooks on all files and not just the changed ones
	pre-commit run --all-file

install_dependencies_locally: ## Install dependencies locally
	pip install -r requirements-dev.txt
	pip install -r requirements.txt

flake8: ## Runs flake8
	flake8 --exculde 'ondewo'

mypy: ## Run mypy static code checking
	pre-commit run mypy --all-files

help: ## Print usage info about help targets
	# (first comment after target starting with double hashes ##)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

makefile_chapters: ## Shows all sections of Makefile
	@echo `cat Makefile| grep "########################################################" -A 1 | grep -v "########################################################"`

TEST:
	@echo ${GITHUB_GH_TOKEN}
	@echo ${PYPI_USERNAME}
	@echo ${PYPI_PASSWORD}
	@echo "\n${CURRENT_RELEASE_NOTES}"

check_build: ## Checks if all built proto-code is there
	@rm -rf build_check.txt
	@for proto in `find ondewo-nlu-api/ondewo -iname "*.proto*"`; \
	do \
		echo $${proto} | cut -d "/" -f 4 | cut -d "." -f 1 >> build_check.txt; \
	done
	@echo "`sort build_check.txt | uniq`" > build_check.txt
	@for file in `cat build_check.txt`;\
	do \
		find ondewo -iname "*pb*" | grep -q $${file}; \
		if test $$? != 0; then  echo "No Proto-Code for $${file}" & exit 1;fi \
	done
	@rm -rf build_check.txt

########################################################
#       Repo Specific Make Targets
########################################################
#		Build

update_setup: ## Update Version in setup.py
	@sed -i "s/version='[0-9]*.[0-9]*.[0-9]*'/version='${ONDEWO_NLU_VERSION}'/g" setup.py
	@sed -i "s/version=\"[0-9]*.[0-9]*.[0-9]*\"/version='${ONDEWO_NLU_VERSION}'/g" setup.py

build: clear_package_data init_submodules checkout_defined_submodule_versions build_compiler generate_ondewo_protos update_setup ## Build source code

push_to_pypi_via_docker: push_to_pypi_via_docker_image  ## Release automation for building and pushing to pypi via a docker image

release_to_github_via_docker: build_utils_docker_image release_to_github_via_docker_image  ## Release automation for building and releasing on GitHub via a docker image

clean_python_api:  ## Clear generated python files
	find ./ondewo -name \*pb2.py -type f -exec rm -f {} \;
	find ./ondewo -name \*pb2_grpc.py -type f -exec rm -f {} \;
	find ./ondewo -name \*.pyi -type f -exec rm -f {} \;
	rm -rf google

build_compiler:  ## Build proto compiler docker image
	make -C ondewo-proto-compiler/python build

generate_ondewo_protos:  ## Generate python code from proto files
	make -f ondewo-proto-compiler/python/Makefile run \
		PROTO_DIR=${ONDEWO_PROTOS_DIR} \
		EXTRA_PROTO_DIR=${GOOGLE_PROTOS_DIR} \
		TARGET_DIR='ondewo' \
		OUTPUT_DIR=${OUTPUT_DIR}


setup_conda_env: ## Checks for CONDA Environment
	@echo "\n START SETTING UP CONDA ENV \n"
	@conda env list | grep -q ondewo-nlu-client-python \
	&& make release || ( echo "\n CONDA ENV FOR REPO DOESNT EXIST \n" \
	&& make create_conda_env)

create_conda_env: ##Creates CONDA Environment
	conda create -y --name ondewo-nlu-client-python python=3.8
	/bin/bash -c 'source `conda info --base`/bin/activate ondewo-nlu-client-python; make setup_developer_environment_locally && echo "\n PRECOMMIT INSTALLED \n"'
	make release

########################################################
#		Release

release: ## Automate the entire release process
	@echo "Start Release"
	make build
	/bin/bash -c 'source `conda info --base`/bin/activate ondewo-nlu-client-python; make precommit_hooks_run_all_files || echo "PRECOMMIT FOUND SOMETHING"'
	git status
	make check_build
	git add ondewo
	git add Makefile
	git add RELEASE.md
	git add setup.py
	git add ${ONDEWO_PROTO_COMPILER_DIR}
	git add ${ONDEWO_NLU_API_DIR}
	git status
	git commit -m "PREPARING FOR RELEASE ${ONDEWO_NLU_VERSION}"
	git push
	make create_release_branch
	make create_release_tag
	make release_to_github_via_docker
	make push_to_pypi_via_docker
	@echo "Release Finished"

create_release_branch: ## Create Release Branch and push it to origin
	git checkout -b "release/${ONDEWO_NLU_VERSION}"
	git push -u origin "release/${ONDEWO_NLU_VERSION}"

create_release_tag: ## Create Release Tag and push it to origin
	git tag -a ${ONDEWO_NLU_VERSION} -m "release/${ONDEWO_NLU_VERSION}"
	git push origin ${ONDEWO_NLU_VERSION}

login_to_gh: ## Login to Github CLI with Access Token
	echo $(GITHUB_GH_TOKEN) | gh auth login -p ssh --with-token

build_gh_release: ## Generate Github Release with CLI
	gh release create --repo $(GH_REPO) "$(ONDEWO_NLU_VERSION)" -n "$(CURRENT_RELEASE_NOTES)" -t "Release ${ONDEWO_NLU_VERSION}"

########################################################
#		Submodules

install: init_submodules ## Installs all packages
	pip install -e .

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

########################################################
#		PYPI

build_package: ## Builds PYPI Package
	python setup.py sdist bdist_wheel
	chmod a+rw dist -R

upload_package: ## Uploads PYPI Package
	twine upload --verbose -r pypi dist/* -u${PYPI_USERNAME} -p${PYPI_PASSWORD}

clear_package_data: ## Clears PYPI Package
	rm -rf build dist ondewo_nlu_client.egg-info

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

push_to_pypi: build_package upload_package clear_package_data ## Builds -> Uploads -> Clears PYPI Package
	@echo 'YAY - Pushed to pypi : )'

show_pypi: build_package ## Shows PYPI Package with Dockerimage
	tar xvfz dist/ondewo-nlu-client-${ONDEWO_NLU_VERSION}.tar.gz
	tree ondewo-nlu-client-${ONDEWO_NLU_VERSION}
	cat ondewo-nlu-client-${ONDEWO_NLU_VERSION}/ondewo_nlu_client.egg-info/requires.txt

show_pypi_via_docker_image: build_utils_docker_image ## Push source code to pypi via docker
	[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	docker run --rm \
		-v ${shell pwd}/dist:/home/ondewo/dist \
		-e PYPI_USERNAME=${PYPI_USERNAME} \
		-e PYPI_PASSWORD=${PYPI_PASSWORD} \
		${IMAGE_UTILS_NAME} make show_pypi
	rm -rf dist

########################################################
#		GITHUB

push_to_gh: login_to_gh build_gh_release ## Logs into GitHub CLI and Releases
	@echo 'Released to Github'

release_to_github_via_docker_image:  ## Release to Github via docker
	docker run --rm \
		-e GITHUB_GH_TOKEN=${GITHUB_GH_TOKEN} \
		${IMAGE_UTILS_NAME} make push_to_gh

########################################################
#		DEVOPS-ACCOUNTS

ondewo_release: spc clone_devops_accounts run_release_with_devops ## Release with credentials from devops-accounts repo
	@rm -rf ${DEVOPS_ACCOUNT_GIT}

clone_devops_accounts: ## Clones devops-accounts repo
	if [ -d $(DEVOPS_ACCOUNT_GIT) ]; then rm -Rf $(DEVOPS_ACCOUNT_GIT); fi
	git clone git@bitbucket.org:ondewo/${DEVOPS_ACCOUNT_GIT}.git

run_release_with_devops: ## Gets Credentials from devops-repo and run release command with them
	$(eval info:= $(shell cat ${DEVOPS_ACCOUNT_DIR}/account_github.env | grep GITHUB_GH & cat ${DEVOPS_ACCOUNT_DIR}/account_pypi.env | grep PYPI_USERNAME & cat ${DEVOPS_ACCOUNT_DIR}/account_pypi.env | grep PYPI_PASSWORD))
	@echo ${CONDA_PREFIX} | grep -q nlu-client-python && make release $(info) || (make setup_conda_env $(info))


spc: ## Checks if the Release Branch, Tag and Pypi version already exist
	$(eval filtered_branches:= $(shell git branch --all | grep "release/${ONDEWO_NLU_VERSION}"))
	$(eval filtered_tags:= $(shell git tag --list | grep "${ONDEWO_NLU_VERSION}"))
	$(eval setuppy_version:= $(shell cat setup.py | grep "version"))
	@if test "$(filtered_branches)" != ""; then echo "-- Test 1: Branch exists!!" & exit 1; else echo "-- Test 1: Branch is fine";fi
	@if test "$(filtered_tags)" != ""; then echo "-- Test 2: Tag exists!!" & exit 1; else echo "-- Test 2: Tag is fine";fi
#	@if test "$(setuppy_version)" != "version='${ONDEWO_NLU_VERSION}',"; then echo "-- Test 3: Setup.py not updated!!" & exit 1; else echo "-- Test 3: Setup.py is fine";fi
