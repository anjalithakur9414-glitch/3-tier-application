 
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDS = "dockerhub-creds"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_FRONTEND = "yashdubey455/ui:${IMAGE_TAG}"
        IMAGE_BACKEND  = "yashdubey455/api:${IMAGE_TAG}"
        SONAR_HOST_URL = "http://SONARQUBE-IP:9000"
        SONAR_PROJECT_KEY = "ui-api-project"
    }
    stages {
        stage('Code Clone') {
            steps {
                git branch: 'master',
                credentialsId: 'github-creds',
                url: 'https://github.com/Yashdubey455/ui-api-db.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                      -Dsonar.projectName=ui-api-project \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_HOST_URL
                    '''
                }
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'docker build -t $IMAGE_BACKEND ./backend'
                sh 'docker build -t $IMAGE_FRONTEND ./frontend'
            }
        }
        stage('Trivy File Scan') {
            steps {
                sh '''
                trivy fs . > trivy-fs-report.txt
                '''
            }
        }
        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image $IMAGE_BACKEND > backend-trivy-report.txt
                trivy image $IMAGE_FRONTEND > frontend-trivy-report.txt
                '''
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }
        stage('Push Images') {
            steps {
                retry(3) {
                    sh '''
                    docker push $IMAGE_BACKEND
                    docker push $IMAGE_FRONTEND
                    '''
                }
            }
        }
        stage('Update Kubernetes Manifest') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                    sed -i "s|image:.*api.*|image: yashdubey455/api:$IMAGE_TAG|g" k8s/backend-deployment.yaml
                    sed -i "s|image:.*ui.*|image: yashdubey455/ui:$IMAGE_TAG|g" k8s/frontend-deployment.yaml
                    git config user.name "jenkins"
                    git config user.email "jenkins@local"
                    git add k8s/
                    git commit -m "update manifests image" || echo "no changes"
                    git push https://$GIT_USER:$GIT_PASS@github.com/Yashdubey455/ui-api-db.git master
                    '''
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '*.txt', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline executed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
 
