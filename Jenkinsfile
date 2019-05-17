    
pipeline {
    agent { docker { image  'wawsinoss/pyodbcpython3.7' } {imgae 'tkinter/get-started'} }
  environment {HOME = '/tmp'} 
  stages {
    // First stage , get files from your GitHub repository.
    stage('Git'){
        steps{
            checkout scm
        }
    }
    stage('build') {
        steps {
        sh 'pip install --user --no-cache-dir -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python UnitTest.py'
      }
      post {
        always {
          junit 'test-reports/*.xml'
        }
      }
    }
  }
}
