import ValidationError from "./ValidationError.js";

class NoTokenError extends ValidationError {
  constructor() {
    super("You did not have provided a token");
    this.name = "NoTokenError";
  }
}

export default NoTokenError;
