import HeaderError from "./HeaderError.js";

class HeaderMalformedError extends HeaderError {
  constructor(header) {
    super("Malformed header: " + header, header);
    this.name = "HeaderMalformedError";
  }
}

export default HeaderMalformedError;
