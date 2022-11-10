FROM node:lts-alpine
RUN npm i -g serve
WORKDIR /app
COPY package*.json ./
RUN npm install
EXPOSE 3000
COPY . .
RUN npm run build
CMD [ "serve", "-s", "dist" ]