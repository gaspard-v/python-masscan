import { check_permission as cp } from "../services/token.js";
import HeaderMalformedError from "../errors/HeaderMalformedError.js";
import UrlMissingBaseError from "../errors/UrlMissingBaseError.js";
import UrlMissingPathError from "../errors/UrlMissingPathError.js";
import TokenPermissionError from "../errors/TokenPermissionError.js";
import NoTokenError from "../errors/NoTokenError.js";

async function parse_token_header(token_header) {
  const [token_type, token] = token_header.split(" ");
  if (!token || !token_type) throw new HeaderMalformedError("authorization");
  if (token_type.toLowerCase() !== "bearer")
    throw new HeaderMalformedError("authorization");
  return token;
}

async function parse_token({ headers, query }) {
  const token_header = headers["authorization"];
  const token_query = query["authorization"];
  if (token_header) return await parse_token_header(token_header);
  if (token_query) return token_query;
  throw new NoTokenError();
}

export async function check_permission(req, res, next) {
  try {
    const token = await parse_token({ headers: req.headers, query: req.query });
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
    const [permitted] = result_token;
    if (!permitted) throw new TokenPermissionError(token, permission);
  } catch (err) {
    next(err);
  }
  next();
}
