import UrlError from "./UrlError.js";

class UrlMissingBaseError extends UrlError {
  constructor(url) {
    super("the url provided does not contain a base", url);
    this.name = "UrlMissingBaseError";
  }
}

export default UrlMissingBaseError;
