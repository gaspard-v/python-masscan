import { check_permission as cp } from "../services/token";

export async function check_permission(req, res, next) {
  try {
    const token_header = req.headers["authorization"];
    if (!token_header) res.send(401, "No token provided");
    const [token_type, token] = token_header.split(" ");
    if (!token) res.send(401);
    const obj = req.baseUrl.substring(1);
    const method = req.path.substring(1);
    const result_token = await cp({
      token: token,
      permission: `${obj}_${method}`,
    });
    if (!result_token) {
      res.send(401, "not permitted");
    }
    next();
  } catch {
    res.send(400, "invalid token");
  }
}
