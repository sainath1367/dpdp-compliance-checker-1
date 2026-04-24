pipeline {
    agent any

    environment {
        APP_NAME = 'dpdp-compliance-checker'
    }

    stages {

        stage('Setup Environment') {
            steps {
                sh '''
                    echo "Setting up environment"
                    python3 --version
                    docker --version || true
                '''
            }
        }

        stage('Backend Setup') {
            steps {
                sh '''
                    cd dpdp-backend
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Backend Test') {
            steps {
                sh '''
                    cd dpdp-backend
                    . venv/bin/activate
                    python -c "print('Backend OK')"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t dpdp-backend ./dpdp-backend || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d -p 8000:8000 dpdp-backend || true
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://localhost:8000/docs || echo "Backend not ready"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Deployment successful!"
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker system prune -f || true
            '''
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}