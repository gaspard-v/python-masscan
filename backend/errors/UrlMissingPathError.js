import UrlError from "./UrlError.js";

class UrlMissingPathError extends UrlError {
  constructor(url) {
    super("the url provided does not contain a path", url);
    this.name = "UrlMissingPathError";
  }
}

export default UrlMissingPathError;
