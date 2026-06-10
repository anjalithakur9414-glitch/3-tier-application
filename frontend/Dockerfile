FROM node:20-alpine

WORKDIR /app

COPY package.json .

RUN npm install
# required details
COPY . .

EXPOSE 3000

CMD ["npm", "start"]

