REM Attention doesn't work in powershell, need to set variables differently
SET NODE_PATH=%AppData%\npm\node_modules
sonar-scanner.bat -D"sonar.projectKey=service_layer_python" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=f5149487d8b17340e0dfaa26292d62dad881fda5"
