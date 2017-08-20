#!groovy

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    parameters {
        booleanParam(name: 'RELEASE_BUILD', defaultValue: false, description: 'Will this be a release build then, sir?')
    }

    stages {

        stage('Prepare') {
            steps {
                sh """
                virtualenv -p /usr/bin/python3 ${env.WORKSPACE}/.venv && \
                source ${env.WORKSPACE}/.venv/bin/activate && \
                pip install -r test-requirements.txt
                pip install -r requirements.txt
                """
            }
        }
        /*
        stage('QA Gate') {
            steps {
                slackSend botUser: true, message: "QA Gate Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                withSonarQubeEnv('jenkins-sonar') {
                    pyBuild(this, "test")
                    sh "${env.SONAR_SCANNER} -Dsonar.branch=${env.BRANCH_NAME} -Dsonar.projectVersion=${pyBuild.version}"
                }
                script {
                    timeout(time: 1, unit: 'HOURS') {
                        def qg = waitForQualityGate()
                        if(qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate failure: ${qg.status}"
                            slackSend botUser: true, message: "QA Gate FAILED - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                        }
                    }
                }
            }
        }
        */
        stage('\uD83D\uDEE0 Build') {
            when { expression { return ! params.RELEASE_BUILD } }
            steps {
                slackSend botUser: true, message: "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                ansiColor('xterm') {
                    pyBuild(this, "test sdist bdist docs")
                    sh ". ${env.WORKSPACE}/.venv/bin/activate && behave"
                }
                script {
                    currentBuild.displayName = "${currentBuild.number}: \uD83D\uDEE0 Build ${pyBuild.version}"
                }
            }
        }
        stage('\uD83C\uDF81 Release') {
            when { expression { return (params.RELEASE_BUILD && (env.BRANCH_NAME == 'develop')) } }
            steps {
                slackSend botUser: true, message: "Release Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                ansiColor('xterm') {

                    //
                    // Force checkout develop and perform an initial test

                    sh "git checkout -f develop"
                    pyBuild(this, "test")
                    sh ". ${env.WORKSPACE}/.venv/bin/activate && behave"

                    //
                    // If the above was successful then clean up, tag the release and perform the release build
                    // Note that it's important to tag it on the develop branch, otherwise subsequent builds won't
                    // recognize the release to have been made

                    sh "git tag -am 'Release ${pyBuild.nextReleaseVersion}' ${pyBuild.nextReleaseVersion}"
                    pyBuild(this, "sdist bdist docs")

                    //
                    // The release was successful, merge with master and push

                    sh "git checkout -f master && git pull && git merge --no-ff develop"

                    //
                    // Upload the release to the Nexus

                    sh 'twine upload -r nexus dist/*'

					//
					// Push master branch and new tag

					sh 'git push && git push --tags'
                }
                script {
                    currentBuild.displayName = "${currentBuild.number}: \uD83C\uDF81 Release ${pyBuild.version}"
                    keepBuild(true)
                }
            }
        }

    }
    post {
        always {
            junit 'build/reports/**/*.xml'
            archive 'dist/mrmat-pictures-*.tar.gz'
            deleteDir()
        }
        success {
            echo "Build is a SUCCESS"
            slackSend botUser: true, message: "Build SUCCESS - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            echo "Build is a FAILURE"
            slackSend botUser: true, message: "Build FAILED - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
    }
}
