import httpStatus from "http-status";
import ExtraPropertyError from "../errors/ExtraPropertyError.js";
import PropertyEnumError from "../errors/PropertyEnumError.js";
import PropertyRequiredError from "../errors/PropertyRequiredError.js";
import PropertyTypeError from "../errors/PropertyTypeError.js";
import HeaderError from "./HeaderError.js";
import TokenPermissionError from "./TokenPermissionError.js";
import UrlError from "./UrlError.js";
import ValidationError from "./ValidationError.js";
import NoTokenError from "./NoTokenError.js";
import FeatureNotImplementedError from "./FeatureNotImplementedError.js";

async function errorHandler(err, req, res, next) {
  if (err instanceof PropertyRequiredError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        property: err.property,
        type: err.expectedType,
      },
    });
  }
  if (err instanceof PropertyEnumError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        property: err.property,
        allowed_values: err.allowedValues,
      },
    });
  }
  if (err instanceof PropertyTypeError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        property: err.property,
        type: err.expectedType,
      },
    });
  }
  if (err instanceof ExtraPropertyError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        property: err.property,
      },
    });
  }
  if (err instanceof ValidationError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
    });
  }
  if (err instanceof HeaderError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        header: err.message,
      },
    });
  }
  if (err instanceof UrlError) {
    return res.status(400).json({
      status: httpStatus["400_NAME"],
      message: err.message,
      details: {
        url: err.url,
      },
    });
  }
  if (err instanceof TokenPermissionError) {
    return res.status(401).json({
      status: httpStatus["401_NAME"],
      message: err.message,
      details: {
        token: err.token,
        permission: err.permission,
      },
    });
  }
  if (err instanceof NoTokenError) {
    return res.status(401).json({
      status: httpStatus["401_NAME"],
      message: err.message,
    });
  }
  if (err instanceof FeatureNotImplementedError) {
    return res.status(500).json({
      status: httpStatus["500_NAME"],
      message: err.message,
    });
  }
  console.error(err);
  return res.status(500).json({
    status: httpStatus["500_NAME"],
    message: "An unknow error has occured",
    details: {
      message: err.message,
    },
  });
}

export default errorHandler;
