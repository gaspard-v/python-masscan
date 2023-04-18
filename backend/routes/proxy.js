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
router.route("/get").get(async (req, res, next) => {
  try {
    const number = req.query.number;
    const result = await get_proxies({ number: number });
    if (!result) {
      res.status(404).send();
      return;
    }
    res.status(200).send(result);
  } catch (err) {
    next(err);
  }
});
export default router;
