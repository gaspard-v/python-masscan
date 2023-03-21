"use strict";
import Express from "express";
import proxy from "./routes/proxy.js";
import token from "./routes/token.js";
import { check_permission } from "./controllers/permission.js";
import * as dotenv from "dotenv";
import httpStatus from "http-status";

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
  res.status(500).json({
    status: httpStatus["500_NAME"],
    message: "An unknow error has occured",
    details: err,
  });
});

app.use("/proxy", check_permission, proxy);
app.use("/token", check_permission, token);

const listen_port = process.env.PORT || 8888;
const listen_host = process.env.LISTEN_HOST || "localhost";
app.listen(listen_port, listen_host, async () => {
  console.log(
    `proxy logger app is listening on address ${listen_host} on port ${listen_port}`
  );
});
