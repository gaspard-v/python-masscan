import { check_permission as cp } from "../services/token.js";
import httpStatus from "http-status";

export async function check_permission(req, res, next) {
  try {
    const token_header = req.headers["authorization"];
    if (!token_header)
      return res.status(400).json({
        status: httpStatus["400_NAME"],
        message: "No Token provided",
        details: [
          {
            header: "authorization",
            message: "authorization header is mandatory",
          },
        ],
      });
    const [token_type, token] = token_header.split(" ");
    if (!token || !token_type)
      return res.status(401).json({
        status: httpStatus["400_NAME"],
        message: "Invalide authorization header",
        details: [
          {
            header: "authorization",
            message:
              "authorization header is present but does not contain a token",
          },
        ],
      });
    const obj = req.baseUrl.substring(1);
    const method = req.path.substring(1);
    if (!obj || !method) {
      const details = [];
      if (!obj)
        details.push({
          url: "missing base",
          message: "the url provided does not contain a valid base",
        });
      if (!method)
        details.push({
          url: "missing path",
          message: "the url provided does not contain a valid path",
        });
      return res.status(400).json({
        status: httpStatus["400_NAME"],
        message: "Invalid request",
        details: details,
      });
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
  } catch (err) {
    res.status(500).json({
      status: httpStatus["500_NAME"],
      message: "An unknow error has occured",
      details: err,
    });
  }
}
