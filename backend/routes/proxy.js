import Express from "express";
import { create_proxy, get_proxies } from "../controllers/proxy.js";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "proxy API online" });
});
router.route("/create").post(async (req, res, next) => {
  try {
    const response = await create_proxy({ body: req.body });
    const [[{ update_count }]] = response;
    if (update_count > 0) return res.status(200).json(response);
    res.status(201).json(response);
  } catch (err) {
    next(err);
  }
});
router.route("/read").get(async (req, res, next) => {
  try {
    const number = req.query.number;
    const inline = req.query.inline;
    const result = await get_proxies({
      number: number,
      inline: inline,
    });
    if (inline) return res.status(200).send(result);
    res.status(200).json(result);
  } catch (err) {
    next(err);
  }
});
export default router;
