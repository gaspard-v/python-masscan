import Express from "express";

const router = Express.Router();

router.route("/").post(async (req, res) => {
  res.send({ reponse: "ok" });
});

export default router;
