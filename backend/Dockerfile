FROM node:lts
WORKDIR /backend
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm i
COPY . .
CMD ["node", "run", "run"]