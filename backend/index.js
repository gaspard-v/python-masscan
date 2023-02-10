"use strict";
import Express from "express";
import proxy from "./routes/proxy.js";
import token from "./routes/token.js";
import { check_permission } from "./controllers/permission.js";
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
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Error");
});

app.use("/token", check_permission);

app.use("/proxy", proxy);
app.use("/token", token);

app.listen(process.env.PORT, async () => {
  console.log(`proxy logger app is listening on port ${process.env.PORT}`);
});
