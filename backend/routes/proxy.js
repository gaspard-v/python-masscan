import Express from "express";

const router = Express.Router();

router.route("/").get(async (req, res) => {
  res.send({ reponse: "ok" });
});

export default router;
