"use strict";
import Express from "express";
import proxy from "./routes/proxy.js";
import token from "./routes/token.js";
import { check_permission } from "./middlewares/permission.js";
import * as dotenv from "dotenv";
import errorHandler from "./errors/errorHandler.js";
import { validateObject } from "./middlewares/type_check.js";

BigInt.prototype.toJSON = function () {
  return this.toString();
};

dotenv.config();

const app = Express();
app.use(Express.json());

if (process.env.DEV) {
  app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Headers", "*");
    next();
  });
}

app.use("/proxy", validateObject, check_permission, proxy);
app.use("/token", validateObject, check_permission, token);
app.use(errorHandler);

const listen_port = process.env.PORT || 8080;
const listen_host = process.env.LISTEN_HOST || "localhost";
app.listen(listen_port, listen_host, async () => {
  console.log(
    `proxy logger app is listening on address ${listen_host} on port ${listen_port}`
  );
});
