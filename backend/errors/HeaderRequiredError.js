import HeaderError from "./HeaderError.js";

class HeaderRequiredError extends HeaderError {
  constructor(header) {
    super("Missing header: " + header, header);
    this.name = "HeaderRequiredError";
  }
}

export default HeaderRequiredError;
