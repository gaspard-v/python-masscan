"use strict";
import Express from "express";

const app = Express();
app.use(Express.json());

app.use((req, res, next) => {
  // use for development only !
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  next();
});
