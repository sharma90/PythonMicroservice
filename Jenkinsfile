pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rs9098/python-microservice"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"   // Jenkins credentials
        GIT_CREDENTIALS_ID = "git-creds"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: "${GIT_CREDENTIALS_ID}",
                    url: 'https://github.com/sharma90/PythonMicroservice.git'
            }
        }

        stage('Generate Version') {
            steps {
                script {
                    if (fileExists('version.txt')) {
                        def version = readFile('version.txt').trim()
                        def num = version.replace("v","").toInteger() + 1
                        env.NEW_VERSION = "v${num}"
                    } else {
                        env.NEW_VERSION = "v1"
                    }

                    writeFile file: 'version.txt', text: env.NEW_VERSION
                    echo "New Version: ${env.NEW_VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${NEW_VERSION} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )]) {
                        sh """
                        echo $PASSWORD | docker login -u $USERNAME --password-stdin
                        docker push ${DOCKER_IMAGE}:${NEW_VERSION}
                        """
                    }
                }
            }
        }

        stage('Update deployment.yaml') {
            steps {
                script {
                    sh """
                    sed -i 's|image: .*|image: ${DOCKER_IMAGE}:${NEW_VERSION}|g' k8s/deployment.yaml
                    """
                }
            }
        }

        stage('Commit & Push Changes') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${GIT_CREDENTIALS_ID}",
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )]) {
                        sh """
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"

                        git add k8s/deployment.yaml version.txt
                        git commit -m "Updated image to ${NEW_VERSION}" || echo "No changes"

                        git push https://${GIT_USER}:${GIT_PASS}@github.com/sharma90/python-microservice.git HEAD:main
                        """
                    }
                }
            }
        }
    }
}