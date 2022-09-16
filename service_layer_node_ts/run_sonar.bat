REM Attention doesn't work in powershell, need to set variables differently
SET NODE_PATH=%AppData%\node_modules
sonar-scanner.bat -D"sonar.projectKey=photo_app_servie_layer_node_ts" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=5726a6d5c8a5efd30a5ce19f763b209b2954ed8b"
