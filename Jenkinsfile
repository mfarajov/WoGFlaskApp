pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'worldofgames'
        CONTAINER_NAME = 'worldofgames-container'
        DOCKER_HUB_REPO = 'muradvalehfarajov/worldofgames'
        GITHUB_REPO = 'https://github.com/mfarajov/WoGFlaskApp.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-pat', url: GITHUB_REPO
            }
        }
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Stop any previously running containers to avoid port conflicts
                    // Ignoring errors if the container doesn't exist
                    bat "docker stop ${env.CONTAINER_NAME} 2>NUL || exit /b 0"
                    bat "docker rm ${env.CONTAINER_NAME} 2>NUL || exit /b 0"

                    // Run the container with specified settings
                    bat "docker run -d --name ${env.CONTAINER_NAME} -p 8777:8777 -v ${env.WORKSPACE}\\Scores.txt:/app/Scores.txt ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Finalize') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        // Use the credentials securely without directly embedding them into the script
                        powershell(script: """
                        \$pass = '${PASS}' | ConvertTo-SecureString -AsPlainText -Force
                        \$cred = New-Object System.Management.Automation.PSCredential ('${USER}', \$pass)
                        echo \$cred.GetNetworkCredential().Password | docker login --username \$cred.UserName --password-stdin
                        """, returnStdout: true).trim()
                    }

                    // Tagging and pushing the Docker image
                    bat "docker tag ${env.DOCKER_IMAGE} ${env.DOCKER_HUB_REPO}:latest"
                    bat "docker push ${env.DOCKER_HUB_REPO}:latest"
                }
            }
        }

    }
    post {
        always {
            // Cleanup after pipeline finishes
            bat "docker rmi ${env.DOCKER_IMAGE} 2>NUL || exit /b 0"
        }
    }
}
