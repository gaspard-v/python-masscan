import UrlQueryError from "./UrlQueryError.js";

class UrlQueryMalformedError extends UrlQueryError {
  constructor(url, query) {
    super("the url provided contains a malformed query", url, query);
    this.name = "UrlQueryMalformedError";
  }
}

export default UrlQueryMalformedError;
