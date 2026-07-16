export
# ---------------- BEFORE RELEASE ----------------
# 1 - Update Version Number
# 2 - Update RELEASE.md
# 3 - make update_setup
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
ONDEWO_NLU_VERSION=7.0.0

ONDEWO_NLU_API_GIT_BRANCH=OND211-2418-add-keycloak-for-2-fa
ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/5.10.0
PYPI_USERNAME?=ENTER_HERE_YOUR_PYPI_USERNAME
PYPI_PASSWORD?=ENTER_HERE_YOUR_PYPI_PASSWORD

# You need to setup an access token at https://github.com/settings/tokens - permissions are important
GITHUB_GH_TOKEN?=ENTER_YOUR_TOKEN_HERE

# Terminate on the ***** separator that delimits release entries, NOT on /\*\*/ — that matched the first
# markdown **bold** span inside the entry and silently truncated the notes there, with no error from
# `gh release create`. Harmless only while no entry used inline bold; the 7.0.0 entry does. Same fix as
# ondewo-nlu-api's Makefile.
CURRENT_RELEASE_NOTES=`cat RELEASE.md \
	| perl -ne 'print if /Release ONDEWO NLU Python Client ${ONDEWO_NLU_VERSION}/../^\*{5}/'`

GH_REPO="https://github.com/ondewo/ondewo-nlu-client-python"
DEVOPS_ACCOUNT_GIT="ondewo-devops-accounts"
DEVOPS_ACCOUNT_DIR="./${DEVOPS_ACCOUNT_GIT}"
ONDEWO_NLU_API_DIR=ondewo-nlu-api
ONDEWO_PROTO_COMPILER_DIR=ondewo-proto-compiler
ONDEWO_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/ondewo/
GOOGLE_PROTOS_DIR=${ONDEWO_NLU_API_DIR}/google/
OUTPUT_DIR=.
IMAGE_UTILS_NAME=ondewo-nlu-client-utils-python:${ONDEWO_NLU_VERSION}
.DEFAULT_GOAL := help

########################################################
#       ONDEWO Standard Make Targets
########################################################

setup_developer_environment_locally: install_uv install_dependencies_locally install_precommit_hooks ## Ready a fresh laptop: install uv, sync runtime+dev deps into .venv, install pre-commit hooks

install_uv: ## Install the uv package manager if it is not already available
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

install_precommit_hooks: ## Installs pre-commit hooks and sets them up for the ondewo-nlu-client-python repo
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

precommit_hooks_run_all_files: ## Runs all pre-commit hooks on all files and not just the changed ones
	uv run pre-commit run --all-files

install_dependencies_locally: ## Install runtime + dev dependencies locally into the uv-managed .venv
	uv sync --extra dev

ruff: ## Lint with ruff (replaces flake8)
	uv run ruff check .

ruff_fix: ## Lint with ruff and auto-fix fixable issues
	uv run ruff check --fix .

ruff_format: ## Format the codebase with ruff (replaces black + autopep8)
	uv run ruff format .

mypy: ## Run mypy static code checking
	uv run mypy ondewo/ tests/

help: ## Print usage info about help targets
	# (first comment after target starting with double hashes ##)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

makefile_chapters: ## Shows all sections of Makefile
	@echo `cat Makefile| grep "########################################################" -A 1 | grep -v "########################################################"`

TEST: ## Prints some important variables
	@echo "Release Notes: \n \n$(CURRENT_RELEASE_NOTES)"
	@echo "GH Token: \t $(if $(GITHUB_GH_TOKEN),<set>,<unset>)"
	@echo "NPM Name: \t $(NPM_USERNAME)"
	@echo "NPM Password: \t $(if $(NPM_PASSWORD),<set>,<unset>)"

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

update_setup: ## Update Version in pyproject.toml
	@perl -i -pe 's/^version = "[0-9]+\.[0-9]+\.[0-9]+"/version = "${ONDEWO_NLU_VERSION}"/' pyproject.toml

build: clear_package_data init_submodules checkout_defined_submodule_versions build_compiler generate_ondewo_protos generate_services update_setup ## Build source code

push_to_pypi_via_docker: push_to_pypi_via_docker_image  ## Release automation for building and pushing to pypi via a docker image

release_to_github_via_docker: build_utils_docker_image release_to_github_via_docker_image  ## Release automation for building and releasing on GitHub via a docker image

clean_python_api:  ## Clear generated python files
	find ./ondewo -name \*pb2.py -type f -exec rm -f {} \;
	find ./ondewo -name \*pb2_grpc.py -type f -exec rm -f {} \;
	find ./ondewo -name \*.pyi -type f -exec rm -f {} \;
	rm -rf google

build_compiler:  ## Build proto compiler docker image
	make -C ondewo-proto-compiler/python build

generate_services: ## Generate service wrapper files from proto definitions
	uv run python ondewo/nlu/scripts/generate_services.py \
		${ONDEWO_NLU_API_DIR}/ondewo/nlu \
		ondewo/nlu/services
	-make precommit_hooks_run_all_files
	make create_async_services
	make precommit_hooks_run_all_files

generate_ondewo_protos:  ## Generate python code from proto files
	make -f ondewo-proto-compiler/python/Makefile run \
		PROTO_DIR=${ONDEWO_PROTOS_DIR} \
		EXTRA_PROTO_DIR=${GOOGLE_PROTOS_DIR} \
		TARGET_DIR='ondewo' \
		OUTPUT_DIR=${OUTPUT_DIR}
	-make precommit_hooks_run_all_files

create_async_services: ## Create async services for all synchronous services
	@find ondewo -type d -name "services" ! -path "*/.*/*" | while read -r dir; do \
	    for file in "$$dir"/*.py; do \
	        filename=$$(basename -- "$$file"); \
	        case "$$filename" in \
	            "__init__.py"|async_*) continue ;; \
	        esac; \
	        cp "$$file" "$$dir/async_$$filename"; \
	    done; \
	    for file in "$$dir"/async_*.py; do \
	        perl -i -pe 'unless(/def stub/){ s/^([[:space:]]*)def /$$1async def /g; s/self\.stub/await self.stub/g; s/ServicesInterface/AsyncServicesInterface/g; s/services_interface/async_services_interface/g; }' \
	            "$$file"; \
	        perl -i -pe \
	            's/\bIterator\b/AsyncIterator/g; s/(response: AsyncIterator\[[^]]+\] = )await (self\.stub)/$$1$$2/g' \
	            "$$file"; \
	    done; \
	done
	cp ondewo/nlu/client.py ondewo/nlu/async_client.py
	perl -i -pe \
	    's/from ondewo\.nlu\.services\.([a-z_]+) import/from ondewo.nlu.services.async_$$1 import/g; s/from ondewo\.utils\.base_client import BaseClient/from ondewo.utils.async_base_client import AsyncBaseClient/g; s/from ondewo\.nlu\.core\.services_container import ServicesContainer/from ondewo.nlu.core.async_services_container import AsyncServicesContainer/g; s/\bServicesContainer\b/AsyncServicesContainer/g; s/\bBaseClient\b/AsyncBaseClient/g; s/class Client\b/class AsyncClient/g' \
	    ondewo/nlu/async_client.py
	cp ondewo/nlu/core/services_container.py ondewo/nlu/core/async_services_container.py
	perl -i -pe \
	    's/from ondewo\.nlu\.services\.([a-z_]+) import/from ondewo.nlu.services.async_$$1 import/g; s/class ServicesContainer\b/class AsyncServicesContainer/g' \
	    ondewo/nlu/core/async_services_container.py
	-make precommit_hooks_run_all_files

########################################################
#		Release

release: ## Automate the entire release process
	@echo "Start Release"
	make build
	-make precommit_hooks_run_all_files
	git status
	make check_build
	git add ondewo
	git add Makefile
	git add RELEASE.md
	git add pyproject.toml uv.lock
	git add ${ONDEWO_PROTO_COMPILER_DIR}
	git add ${ONDEWO_NLU_API_DIR}
	git status
	-git commit --no-verify -m "PREPARING FOR RELEASE ${ONDEWO_NLU_VERSION}"
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
	@echo $(GITHUB_GH_TOKEN) | gh auth login -p ssh --with-token

build_gh_release: ## Generate Github Release with CLI
	gh release create --repo $(GH_REPO) "$(ONDEWO_NLU_VERSION)" -n "$(CURRENT_RELEASE_NOTES)" -t "Release ${ONDEWO_NLU_VERSION}"

########################################################
#		Submodules

install: init_submodules ## Installs all packages
	uv sync --extra dev

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
	uv build
	chmod a+rw dist -R

upload_package: ## Uploads PYPI Package
	@twine upload --verbose -r pypi dist/* -u${PYPI_USERNAME} -p${PYPI_PASSWORD}

clear_package_data: ## Clears PYPI Package
	echo "Waiting 5s so directory for removal is not busy anymore"
	sleep 5s
	-rm -rf build dist ondewo_nlu_client.egg-info

build_utils_docker_image:  ## Build utils docker image
	docker build -f Dockerfile.utils -t ${IMAGE_UTILS_NAME} .

push_to_pypi_via_docker_image:  ## Push source code to pypi via docker
	[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	@docker run --rm \
		-v ${shell pwd}/dist:/home/ondewo/dist \
		-e PYPI_USERNAME=${PYPI_USERNAME} \
		-e PYPI_PASSWORD=${PYPI_PASSWORD} \
		${IMAGE_UTILS_NAME} make push_to_pypi
	rm -rf dist

push_to_pypi: build_package upload_package clear_package_data ## Builds -> Uploads -> Clears PYPI Package
	@echo 'YAY - Pushed to pypi : )'

show_pypi: build_package ## Shows PYPI Package with Dockerimage
	tar xvfz dist/ondewo_nlu_client-${ONDEWO_NLU_VERSION}.tar.gz
	tree ondewo_nlu_client-${ONDEWO_NLU_VERSION}
	cat ondewo_nlu_client-${ONDEWO_NLU_VERSION}/ondewo_nlu_client.egg-info/requires.txt

show_pypi_via_docker_image: build_utils_docker_image ## Push source code to pypi via docker
	[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	@docker run --rm \
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
	@docker run --rm \
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
	make release $(info)


spc: ## Checks if the Release Branch, Tag and Pypi version already exist
	$(eval filtered_branches:= $(shell git branch --all | grep "release/${ONDEWO_NLU_VERSION}"))
	$(eval filtered_tags:= $(shell git tag --list | grep "${ONDEWO_NLU_VERSION}"))
	$(eval pyproject_version:= $(shell grep '^version = ' pyproject.toml))
	@if test "$(filtered_branches)" != ""; then echo "-- Test 1: Branch exists!!" & exit 1; else echo "-- Test 1: Branch is fine";fi
	@if test "$(filtered_tags)" != ""; then echo "-- Test 2: Tag exists!!" & exit 1; else echo "-- Test 2: Tag is fine";fi
	#	@if test "$(pyproject_version)" != "version = \"${ONDEWO_NLU_VERSION}\""; then echo "-- Test 3: pyproject.toml not updated!!" & exit 1; else echo "-- Test 3: pyproject.toml is fine";fi
