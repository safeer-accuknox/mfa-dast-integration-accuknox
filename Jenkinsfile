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
                git 'https://github.com/safeer-accuknox/mfa-dast-integration-accuknox'  // Replace with your repository URL
            }
        }
        stage('Run Python container for updating MFA') {
            steps {
                script {
                    sh '''
                    docker run -d -it --rm -v /var/jenkins_home/workspace/Accuknox-DAST/:/wrk/:rw python:3.11-slim /bin/bash -c "pip install --no-cache-dir pyotp && python /wrk/scripts/mfa-gen.py"
                    '''
                }
            }
        }
        stage('List all files') {
            steps {
                script {
                    sh '''
                    pwd
                    ls -lahR
                    cat scripts/mfa
                    '''
                }
            }
        }
        stage('Run ZAP container') {
            steps {
                script {
                    sh '''
                    docker run --rm -v /var/jenkins_home/workspace/Accuknox-DAST/:/zap/wrk/:rw -u zap -i ghcr.io/zaproxy/zaproxy:stable zap.sh -addoninstall communityScripts -addoninstall jython -loglevel debug -cmd -autorun /zap/wrk/config-mfa.yaml
                    '''
                }
            }
        }
        stage('Upload Scan Results') {
            steps {
                script {
                    sh '''
                    curl --location --request POST "https://${END_POINT}/api/v1/artifact/?tenant_id=${TENANT_ID}&data_type=ZAP&label_id=${LABEL}&save_to_s3=false" --header "Tenant-Id: ${TENANT_ID}" --header "Authorization: Bearer ${TOKEN}" --form 'file=@"report.json"'
                    '''
                }
            }
        }
    }
}
