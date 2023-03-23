import Express from "express";
import { create_proxy } from "../controllers/proxy.js";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "proxy API online" });
});
router.route("/create").post(async (req, res) => {
  const response = await create_proxy({ body: req.body });
  const [[{ update_count }]] = response;
  if (update_count > 0) return res.status(200).json(response);
  res.status(201).json(response);
});

export default router;
