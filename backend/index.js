"use strict";
import Express from "express";
import { createPool } from "mariadb";

const app = Express();
app.use(Express.json());

const database = createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  connectionLimit: 100,
});

app.use((req, res, next) => {
  // use for development only !
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  next();
});
