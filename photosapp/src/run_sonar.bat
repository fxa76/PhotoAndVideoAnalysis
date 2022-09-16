REM Attention doesn't work in powershell, need to set variables differently
SET NODE_PATH=%AppData%\npm\node_modules
sonar-scanner.bat -D"sonar.projectKey=photos_app_angular" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=969dd6d14a0e53f558ff299eaa93e826b09f15b9"
