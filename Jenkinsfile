pipeline {
    agent any
    environment {
        TOKEN = credentials('ACCUKNOX_TOKEN')
        END_POINT = 'cspm.demo.accuknox.com'
        TENANT_ID = '167'
        LABEL = 'SPOC'
    }
    stages {
        stage('Checkout Repository') {
            steps {
                git 'https://github.com/safeer-accuknox/mfa-dast-integration-accuknox.git'
            }
        }
        stage('Run Python container for updating MFA') {
            steps {
                script {
                    docker.image('python:3.11-slim').inside('-v $(pwd):/wrk/:rw') {
                        sh 'pip install --no-cache-dir pyotp && python /wrk/scripts/mfa-gen.py'
                    }
                }
            }
        }
        stage('Run ZAP container') {
            steps {
                script {
                    docker.image('ghcr.io/zaproxy/zaproxy:stable').inside('-v $(pwd):/zap/wrk/:rw -u zap') {
                        sh 'zap.sh -addoninstall communityScripts -addoninstall jython -loglevel debug -cmd -autorun /zap/wrk/config-mfa.yaml'
                    }
                }
            }
        }
        stage('Upload Scan Results') {
            steps {
                script {
                    sh '''
                    curl --location --request POST "https://${END_POINT}/api/v1/artifact/?tenant_id=${TENANT_ID}&data_type=ZAP&label_id=${LABEL}&save_to_s3=false" \
                    --header "Tenant-Id: ${TENANT_ID}" --header "Authorization: Bearer ${TOKEN}" --form 'file=@"report.json"'
                    '''
                }
            }
        }
    }
}
