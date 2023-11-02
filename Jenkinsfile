pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        environment {
            DB_JSON = credentials('DB_JSON_ID')  // ID는 앞서 생성한 자격 증명의 ID입니다.
            MAIL_JSON = credentials('MAIL_JSON_ID')
            SECRET_JSON = credentials('SECRET_JSON_ID')
            SSH_JSON = credentials('SSH_JSON_ID')
        }

        stages {
            stage('Use Secrets') {
                steps {
                    script {
                        // 이제 환경 변수를 통해 DB_JSON 값을 사용할 수 있습니다.
                        writeFile file: '.secrets/db.json', text: env.DB_JSON
                        writeFile file: '.secrets/mail.json', text: env.MAIL_JSON
                        writeFile file: '.secrets/secret.json', text: env.SECRET_JSON
                        writeFile file: '.secrets/ssh.json', text: env.SSH_JSON
                    }
                }
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
