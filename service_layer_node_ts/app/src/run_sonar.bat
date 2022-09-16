REM Attention doesn't work in powershell, need to set variables differently
SET NODE_PATH=%AppData%\npm\node_modules
sonar-scanner.bat -D"sonar.projectKey=photo_app_servie_layer_node_ts" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=98f0f31b00dda121312b93f372b3d23c72b05e94"