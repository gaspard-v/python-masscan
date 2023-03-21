import Express from "express";
import { create_proxy } from "../controllers/proxy.js";
import httpStatus from "http-status";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "proxy API online" });
});
router.route("/create").post(async (req, res) => {
  try {
    const response = await create_proxy({ body: req.body });
    const [[{ update_count }]] = response;
    if (update_count > 0) return res.status(200).json(response);
    res.status(201).json(response);
  } catch (err) {
    if (err instanceof TypeError) {
      return res.status(400).json({
        status: httpStatus["400_NAME"],
        message: "Missing property",
        details: {
          message: err.message,
        },
      });
    }
    return res.status(500).json({
      status: httpStatus["500_NAME"],
      message: "Unknown error",
      details: {
        message: err.message,
      },
    });
  }
});

export default router;
