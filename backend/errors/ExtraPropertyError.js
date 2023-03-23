import PropertyError from "./propertyError.js";

class ExtraPropertyError extends PropertyError {
  constructor(property) {
    super("Unexpeted extra property: " + property, property);
    this.name = "ExtraPropertyError";
  }
}

export default ExtraPropertyError;
