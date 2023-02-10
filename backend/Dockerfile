FROM node:lts
WORKDIR /backend
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm i
EXPOSE 8888
COPY . .
CMD ["npm", "run", "run"]