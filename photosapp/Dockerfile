FROM node:16.14

WORKDIR /app

COPY . .

RUN npm install --save-dev @angular-devkit/build-angular
RUN npm install -g @angular/cli@15
RUN npm install 

EXPOSE 4200 49153

CMD ["npm","start"]
