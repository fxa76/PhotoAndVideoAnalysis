1. build the container 
```
docker build -t sslgen .
```

2. run the container in interactive mode
```
docker run -it -v c/cert:/cert --rm  sslgen /bin/bash
```

3. in the container 
cd cert
openssl genpkey -algorithm RSA -des3 -out private-key.pem -pkeyopt rsa_keygen_bits:4096
openssl req -new -key private-key.pem -out csr.pem
openssl x509 -in csr.pem -out certificate.pem -req -signkey private-key.pem -days 365

if you answered the questions certificates shoudl be available on c:\cert forlder
