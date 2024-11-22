pipeline {
    agent any
    environment {
        TOKEN = 'ACCUKNOX_TOKEN'
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
                    try {
                        docker.image('python:3.11-slim').inside('-v $(pwd):/wrk/:rw') {
                            sh 'pip install --no-cache-dir pyotp && python /wrk/scripts/mfa-gen.py'
                        }
                    } catch (Exception e) {
                        error "Error in Python container for MFA update: ${e.message}"
                    }
                }
            }
        }

    }
}
