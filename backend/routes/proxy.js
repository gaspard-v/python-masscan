import Express from "express";

import { create_proxy } from "../controllers/proxy.js";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "API online" });
});

router.route("/create").get(async (req, res) => {
  res.send(create_proxy(req.body));
});

export default router;
