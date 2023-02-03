"use strict";
import Express from "express";
import proxy from "./routes/proxy.js";
import * as dotenv from "dotenv";

dotenv.config();

const app = Express();
app.use(Express.json());

app.use((req, res, next) => {
  // use for development only !
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  next();
});

app.use("/proxy", proxy);

app.listen(process.env.PORT, async () => {
  console.log(`proxy logger app is listening on port ${process.env.PORT}`);
});
