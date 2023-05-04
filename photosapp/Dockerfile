FROM node:14

WORKDIR /app

COPY . .

RUN npm install --save-dev @angular-devkit/build-angular
RUN npm install -g @angular/cli

EXPOSE 4200 49153

CMD ["npm","start"]
