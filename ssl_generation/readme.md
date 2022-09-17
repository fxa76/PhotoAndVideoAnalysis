Instructions to create a self signed certificate 

1. build the container 
```
docker build -t sslgen .
```

2. run the container in interactive mode
```
docker run -it -v c/cert:/cert --rm  sslgen /bin/bash
```

3. in the container 
```
cd cert
openssl req -new -newkey rsa:2048 -nodes -out FXA.csr -keyout FXA.key
openssl x509 -in FXA.csr -out certificate.pem -req -signkey FXA.key -days 365
```

if you answered the questions certificates shoudl be available on c:\cert forlder copy the files in docker-nginx/certificate folder
