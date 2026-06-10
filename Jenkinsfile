pipeline {
    agent any 
    
    environment {
        DOCKERHUB_CREDS = "dockerhub-creds"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_BACKEND = "yashdubey455/api:${IMAGE_TAG}"
        IMAGE_FRONTEND = "yashdubey455/ui:${IMAGE_TAG}"
    }
    
    stages {
        stage('code') {
            steps{
                git branch: 'master',
                credentialsId: 'github-creds',
                url: 'https://github.com/Yashdubey455/ui-api-db.git'
            }
        }
        // pipelines
        stage('build') {
            steps{
                sh 'docker build -t $IMAGE_BACKEND ./backend'
                sh 'docker build -t $IMAGE_FRONTEND ./frontend'
            }
        }
        stage('login'){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
            }
        }
        stage('push'){
           steps {

            retry(3) {

              sh '''
                docker push $IMAGE_BACKEND
                docker push $IMAGE_FRONTEND
               '''
           }
        }
}
        stage('update manifest'){
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
}
