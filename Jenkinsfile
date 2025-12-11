pipeline {
    agent any
    
    environment {
        // For TESTING - only your email
        STUDENT_EMAIL = 'areebaniazi26@gmail.com'
        // PROFESSOR_EMAIL = 'qasimamlik@gmail.com'  // Commented out for testing
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh '''
                    echo "========================================"
                    echo "🚀 DEVOPS ASSIGNMENT - TEST BUILD"
                    echo "========================================"
                    echo "Student: Areeba Niazi"
                    echo "Course: CSC483 - DevOps"
                    echo "Build #${BUILD_NUMBER}"
                    echo "Repository: ${GIT_URL}"
                    echo "========================================"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('selenium-tests') {
                    sh '''
                        echo "🐳 Building Docker image..."
                        docker build -t mern-selenium-tests:latest .
                        echo "✅ Docker image built successfully"
                    '''
                }
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    echo "🧪 Running 12 Selenium tests in Docker..."
                    
                    # Create directory for test results
                    mkdir -p ${WORKSPACE}/test-results
                    
                    # Run tests in Docker container
                    docker run --rm \
                        --name selenium-tests \
                        --shm-size=2g \
                        -v ${WORKSPACE}/test-results:/app/test-results \
                        mern-selenium-tests:latest \
                        python -m pytest tests/ -v \
                            --html=/app/test-results/report.html \
                            --self-contained-html \
                            --junitxml=/app/test-results/junit-results.xml
                    
                    echo "✅ Tests completed in Docker container"
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                sh '''
                    echo "📊 Copying test reports and screenshots..."
                    
                    # Copy any existing screenshots
                    mkdir -p ${WORKSPACE}/screenshots
                    cp selenium-tests/ss/*.png ${WORKSPACE}/screenshots/ 2>/dev/null || echo "No screenshots to copy"
                    
                    echo "✅ Reports ready"
                '''
            }
        }
    }
    
    post {
        always {
            // Publish HTML report
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-results',
                reportFiles: 'report.html',
                reportName: 'Selenium Test Report'
            ])
            
            // Archive artifacts
            archiveArtifacts artifacts: 'test-results/*, screenshots/*', allowEmptyArchive: true
            
            // Cleanup Docker containers
            sh '''
                echo "🧹 Cleaning up..."
                docker rm -f selenium-tests 2>/dev/null || true
            '''
        }
        
        success {
            // TEST EMAIL - Send to yourself only
            emailext(
                subject: "✅ TEST SUCCESS: DevOps Assignment - Build #${BUILD_NUMBER}",
                body: """
                ========================================
                ✅ JENKINS PIPELINE TEST - SUCCESS
                ========================================
                
                This is a TEST email to verify Jenkins email configuration.
                
                Details:
                - Student: Areeba Niazi
                - Build: #${BUILD_NUMBER}
                - Status: ${currentBuild.currentResult}
                - Duration: ${currentBuild.durationString}
                
                ✅ 12 Selenium test cases executed successfully
                ✅ Docker containerization working
                ✅ Jenkins pipeline automation functional
                
                ========================================
                LINKS FOR VERIFICATION:
                ========================================
                Test Report: ${BUILD_URL}HTML_Report/
                Build Details: ${BUILD_URL}
                Console Output: ${BUILD_URL}console
                
                ========================================
                NOTE: This is a TEST. 
                Final submission will be sent to Professor Qasim Malik.
                ========================================
                """,
                to: '${env.STUDENT_EMAIL}',
                mimeType: 'text/plain'
            )
            
            echo "✅ TEST email sent to ${env.STUDENT_EMAIL}"
        }
        
        failure {
            emailext(
                subject: "❌ TEST FAILED: DevOps Assignment - Build #${BUILD_NUMBER}",
                body: """
                ========================================
                ❌ JENKINS PIPELINE TEST - FAILED
                ========================================
                
                Jenkins pipeline failed during testing.
                
                Build: #${BUILD_NUMBER}
                Failed Stage: ${STAGE_NAME}
                
                Please check: ${BUILD_URL}console
                """,
                to: '${env.STUDENT_EMAIL}',
                mimeType: 'text/plain'
            )
            
            echo "❌ Failure email sent to ${env.STUDENT_EMAIL}"
        }
    }
}