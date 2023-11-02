pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '/usr/bin/docker build --tag ethanall94/wonjo_omg .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                        sh '/usr/bin/docker push ethanall94/wonjo_omg'
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh '/usr/bin/docker pull ethanall94/wonjo_omg'
                    // 아래의 명령은 새로운 컨테이너를 실행하기 전에 이전 컨테이너를 중지하고 제거합니다.
                    sh '(/usr/bin/docker stop omg_container || true) && (/usr/bin/docker rm omg_container || true)'
                    sh '/usr/bin/docker run -d -p 80:8000 --name omg_container ethanall94/wonjo_omg'
                }
            }
        }
    }
}
