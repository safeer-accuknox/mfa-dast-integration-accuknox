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
        stage('foo') {
            steps {
                sh "docker version" // DOCKER_CERT_PATH is automatically picked up by the Docker client
            }
        }

    }
}
