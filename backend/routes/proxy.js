import Express from "express";

import { create_proxy } from "../controllers/proxy.js";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "proxy API online" });
});
router.route("/create").get(async (req, res) => {
  const [success, response] = await create_proxy(req.body);
  if (!success) {
    res.send(403, response);
    return;
  }
  res.send(response);
});

export default router;
