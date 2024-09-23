FROM node:10.16.0


# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY ./app/*.json /app/
# Bundle app source
COPY ./app /app/

WORKDIR /app
RUN npm install
# If you are building your code for production
# RUN npm ci --only=production



EXPOSE 2344
CMD [ "npm", "dev" ]
