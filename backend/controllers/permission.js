import { check_permission as cp } from "../services/token.js";
import HeaderRequiredError from "../errors/HeaderRequiredError.js";
import HeaderMalformedError from "../errors/HeaderMalformedError.js";
import UrlMissingBaseError from "../errors/UrlMissingBaseError.js";
import UrlMissingPathError from "../errors/UrlMissingPathError.js";
import TokenPermissionError from "../errors/TokenPermissionError.js";

export async function check_permission(req, res, next) {
  try {
    const token_header = req.headers["authorization"];
    if (!token_header) throw new HeaderRequiredError("authorization");
    const [token_type, token] = token_header.split(" ");
    if (!token || !token_type) throw new HeaderMalformedError("authorization");
    const obj = req.baseUrl.substring(1);
    const method = req.path.substring(1);
    if (!obj || !method) {
      if (!obj) throw new UrlMissingBaseError(req.baseUrl);
      if (!method) throw new UrlMissingPathError(req.path);
    }
    const permission = `${obj}_${method}`;
    const result_token = await cp({
      token: token,
      permission: permission,
    });
    if (!result_token) throw new TokenPermissionError(token, permission);
  } catch (err) {
    next(err);
  }
  next();
}
