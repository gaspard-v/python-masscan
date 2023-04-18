import UrlError from "./UrlError.js";

class UrlQueryError extends UrlError {
  constructor(message, url, query) {
    super(message, url);
    this.query = query;
    this.name = "UrlQueryError";
  }
}

export default UrlQueryError;
