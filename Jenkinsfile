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
        stage('Check Python') {
            steps {
        bat "C:\\Users\\Ravi\\AppData\\Local\\Programs\\Python\\Python314\\python.exe --version"
        }
        }

        stage('Test') {
           steps {
            bat """
             C:\\Users\\Ravi\\AppData\\Local\\Programs\\Python\\Python314\\python.exe -m pytest --cov=app --cov-report=xml
            """
        }
        }

        stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('SonarQube') {
            bat """
            sonar-scanner ^
              -Dsonar.projectKey=python-microservice ^
              -Dsonar.sources=app ^
              -Dsonar.python.coverage.reportPaths=coverage.xml
            """
        }
    }
}

        stage('Quality Gate') {
              steps {
                    timeout(time: 5, unit: 'MINUTES') { 
                    waitForQualityGate abortPipeline: true
                }
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
                    bat "docker build -t ${DOCKER_IMAGE}:${NEW_VERSION} ."
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
                        bat """
                        docker login -u %USERNAME% -p %PASSWORD%
                        docker push ${DOCKER_IMAGE}:${NEW_VERSION}
                        """
                    }
                }
            }
        }

         stage('Update deployment.yaml') {
           steps {
                script {
                    powershell """
            (Get-Content k8s/deployment.yaml) -replace 'image: .*', 'image: ${env.DOCKER_IMAGE}:${env.NEW_VERSION}' | Set-Content k8s/deployment.yaml
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
                        bat """
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"

                        git add k8s/deployment.yaml version.txt
                        git commit -m "Updated image to ${NEW_VERSION}" || echo "No changes"

                        git push https://${GIT_USER}:${GIT_PASS}@github.com/sharma90/PythonMicroservice.git HEAD:main
                        """
                    }
                }
            }
        }
    }
}