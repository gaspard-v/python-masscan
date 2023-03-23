import { check_permission as cp } from "../services/token.js";
import httpStatus from "http-status";
import HeaderRequiredError from "../errors/HeaderRequiredError.js";
import HeaderMalformedError from "../errors/HeaderMalformedError.js";
import UrlMissingBaseError from "../errors/UrlMissingBaseError.js";
import UrlMissingPathError from "../errors/UrlMissingPathError.js";

export async function check_permission(req, res, next) {
  const token_header = req.headers["authorization"];
  if (!token_header) throw new HeaderRequiredError("authorization");
  const [token_type, token] = token_header.split(" ");
  if (!token || !token_type) throw new HeaderMalformedError("authorization");
  const obj = req.baseUrl.substring(1);
  const method = req.path.substring(1);
  if (!obj || !method) {
    if (!obj) throw new UrlMissingBaseError(req.baseUrl);
    if (!method) throw details.push(new UrlMissingPathError(req.path));
  }
  const result_token = await cp({
    token: token,
    permission: `${obj}_${method}`,
  });
  if (!result_token)
    return res.status(400).json({
      status: httpStatus["401_NAME"],
      message: httpStatus["401"],
      details: [
        {
          token: token,
          message:
            "you are not authorized to perform this action with the given token",
        },
      ],
    });
  next();
}
