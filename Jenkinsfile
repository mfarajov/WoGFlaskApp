pipeline {

    agent any

    environment {
        DOCKER_IMAGE = 'worldofgames'
        CONTAINER_NAME = 'worldofgames-container'
        DOCKER_HUB_REPO = 'muradvalehfarajov/worldofgames'
        // IMAGE_TAG = "build-${BUILD_NUMBER}"
        IMAGE_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
        // IMAGE_TAG = "v1.0.0"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master']],
                    extensions: [],
                    userRemoteConfigs: [
                        [
                            credentialsId: 'githubcredentials',
                            url: 'git@github.com:mfarajov/WoGFlaskApp.git'
                        ]
                    ]
                ])
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    // Create or update the .env file with the current IMAGE_TAG for docker-compose to use
                    bat "echo IMAGE_TAG=${env.IMAGE_TAG} > .env"
                }
            }
        }

        stage('Build and Run') {
            steps {
                script {
                    //bat "docker-compose -p ${DOCKER_IMAGE} up --build -d"

                    // Build the Docker image with the dynamically generated tag
                    bat "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
                    // Up the docker-compose project with the new image
                    bat "docker-compose -p ${DOCKER_IMAGE} up -d"
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        // Login to Docker Hub using PowerShell
                        powershell(script: """
                        \$pass = '${PASS}' | ConvertTo-SecureString -AsPlainText -Force
                        \$cred = New-Object System.Management.Automation.PSCredential ('${USER}', \$pass)
                        echo \$cred.GetNetworkCredential().Password | docker login --username \$cred.UserName --password-stdin
                        """, returnStdout: true).trim()
                    }
                    bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        always {
            script {
            bat "docker-compose -p ${DOCKER_IMAGE} down"
            bat "docker rmi ${DOCKER_HUB_REPO}:${IMAGE_TAG} || exit /b 0"
            }
        }
    }
}
