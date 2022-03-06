pipeline {
    agent any
    parameters {
        string(name: 'ONDEWO_NLU_CLIENT_PYTHON', defaultValue: 'ondewo-nlu-client-python', description: 'root')
        string(name: 'ONDEWO_NLU_API', defaultValue: 'ondewo-nlu-api', description: 'Git submodule for nlu api')
        string(name: 'ONDEWO_NLU_CLIENT_DIR', defaultValue: 'ondewo', description: 'Directory of generated client files')
        string(name: 'ONDEWO_TEST_DIR', defaultValue: 'ondewo-test', description: 'Directory for newly created client app')
        string(name: 'ONDEWO_PROTOS_DIR', defaultValue: 'ondewo-nlu-api/ondewo', description: 'Directory for ondewo proto files')
        string(name: 'GOOGLE_PROTOS_DIR', defaultValue: 'ondewo-nlu-api/googleapis/google/', description: 'Directory for google proto files')
        string(name: 'GITHUB_TOKEN', defaultValue: '', description: '')
        string(name: 'ONDEWO_USER', defaultValue: 'ondewo', description: 'Github user hosting the repositories')
        string(name: 'BRANCH_TO_PULL', defaultValue: 'master', description: 'Create pull request for this branch ath the end')
        string(name: 'BRANCH_NAME', defaultValue: '', description: 'Branch name of the nlu api repository to checkout')
        string(name: 'BRANCH_NAME_STARTS', defaultValue: 'release', description: 'Build only branches that start with this substring')
    }
    
            
    stages {
        stage('Branch check') {
            when {
                expression {
                    return !(params.BRANCH_NAME ==~ /.*${params.BRANCH_NAME_STARTS}.*/)
                }
            }
            steps {
                error "Branch ${params.BRANCH_NAME} is ingored"
            }
        }
        stage('Build') {
            environment {
                BRANCH_NAME = "${(params.BRANCH_NAME =~ /.*(${params.BRANCH_NAME_STARTS}.*)/)[0][1]}"
            }
            steps {
                sh """
                    echo "Working with branch ${BRANCH_NAME}";
                    rm -rf ${params.ONDEWO_NLU_CLIENT_PYTHON};
                    git clone -b ${params.BRANCH_TO_PULL} https://${params.GITHUB_TOKEN}@github.com/${params.ONDEWO_USER}/${params.ONDEWO_NLU_CLIENT_PYTHON}.git;
                    cd ${params.ONDEWO_NLU_CLIENT_PYTHON};
                    git config --file=.gitmodules submodule.${params.ONDEWO_NLU_API}.url https://${params.GITHUB_TOKEN}@github.com/${params.ONDEWO_USER}/${params.ONDEWO_NLU_API}.git;
                    git submodule sync;
                    git submodule update --init;
                    cd ${params.ONDEWO_NLU_API};
                    git checkout ${BRANCH_NAME};
                    cd ..;
                    mkdir -p ${params.ONDEWO_TEST_DIR};
                    ONDEWO_NLU_CLIENT_DIR=`basename ${params.ONDEWO_PROTOS_DIR}`;
                    GOOGLE_DIR_BASE=`basename ${params.GOOGLE_PROTOS_DIR}`;
                    CONTAINER_NAME=`basename ${BRANCH_NAME}`;
                    docker build --network=host -t ondewo-python-proto-compiler ./ondewo-proto-compiler/python;
                    docker run \
                            --rm --name \${CONTAINER_NAME} \
                            -v ${WORKSPACE}/${params.ONDEWO_NLU_CLIENT_PYTHON}/${params.ONDEWO_TEST_DIR}:/home/ondewo/ondewo-proto-compiler/output \
                            -v ${WORKSPACE}/${params.ONDEWO_NLU_CLIENT_PYTHON}/${params.ONDEWO_PROTOS_DIR}:/home/ondewo/ondewo-proto-compiler/protos/\${ONDEWO_NLU_CLIENT_DIR} \
                            -v ${WORKSPACE}/${params.ONDEWO_NLU_CLIENT_PYTHON}/${params.GOOGLE_PROTOS_DIR}:/home/ondewo/ondewo-proto-compiler/protos/\${GOOGLE_DIR_BASE} \
                            -e INTERNAL_TARGET_PROTO_DIR= \
                            ondewo-python-proto-compiler;
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                    cd ${params.ONDEWO_NLU_CLIENT_PYTHON};
                    ONDEWO_NLU_CLIENT_DIR=`basename ${params.ONDEWO_PROTOS_DIR}`;
                    ./test_pb_files \${ONDEWO_NLU_CLIENT_DIR} \
                        ${params.ONDEWO_TEST_DIR}/\${ONDEWO_NLU_CLIENT_DIR}
                """
            }
        }
        stage('Deploy') {
            environment {
                BRANCH_NAME = "${(params.BRANCH_NAME =~ /.*(${params.BRANCH_NAME_STARTS}.*)/)[0][1]}"
            }
            steps {
                echo 'Test passed, commit changes'
                sh """
                    cd ${params.ONDEWO_NLU_CLIENT_PYTHON};
                    git checkout -f ${BRANCH_NAME} || git checkout -b ${BRANCH_NAME};
                    ONDEWO_NLU_CLIENT_DIR=`basename ${params.ONDEWO_PROTOS_DIR}`;
                    cp -rf ${params.ONDEWO_TEST_DIR}/\${ONDEWO_NLU_CLIENT_DIR}/* \
                        \${ONDEWO_NLU_CLIENT_DIR};
                    git add \${ONDEWO_NLU_CLIENT_DIR};
                    git add ${params.ONDEWO_NLU_API};
                    git config --global user.name 'jenkins';
                    git config --global user.email 'jenkins@jenkins.com';
                    git commit -m "update api and client files";
                    git push --set-upstream origin ${BRANCH_NAME};
                """
            }
        }
        stage('Create pull request') {
            environment {
                BRANCH_NAME = "${(params.BRANCH_NAME =~ /.*(${params.BRANCH_NAME_STARTS}.*)/)[0][1]}"
            }
            steps {
                echo "Create pull request ${BRANCH_NAME} --> ${params.BRANCH_TO_PULL}"
                sh """
                    curl \
                    -X POST \
                    -H "Accept: application/vnd.github.v3+json" \
                     https://${params.GITHUB_TOKEN}@api.github.com/repos/${params.ONDEWO_USER}/${params.ONDEWO_NLU_CLIENT_PYTHON}/pulls \
                    -d '{"head": "${BRANCH_NAME}", "base": "${params.BRANCH_TO_PULL}", "title": "generated from jenkins pipeline: ${BRANCH_NAME}"}';
                """
            }
        }
    }
}
