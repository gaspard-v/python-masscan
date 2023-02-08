import Express from "express";

import { get_permission } from "../controllers/token.js";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "token API online" });
});

router.route("/:token").get(async (req, res) => {
  res.send(await get_permission(req.params.token));
});

export default router;
