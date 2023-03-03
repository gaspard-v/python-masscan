import { check_permission as cp } from "../services/token";

export async function check_permission(req, res, next) {
  try {
    const token_header = req.headers["authorization"];
    if (!token_header) return res.send(401, "no token provided");
    const [token_type, token] = token_header.split(" ");
    if (!token || !token_type)
      return res.send(401, "invalide authorization header");
    const obj = req.baseUrl.substring(1);
    const method = req.path.substring(1);
    if (!obj || !method) return res.send(400, "invalid request");
    const result_token = await cp({
      token: token,
      permission: `${obj}_${method}`,
    });
    if (!result_token) return res.send(401, "not permitted");
    next();
  } catch {
    res.send(500, "serveur error");
  }
}
