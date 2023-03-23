import PropertyError from "./propertyError.js";

class PropertyRequiredError extends PropertyError {
  constructor(property, expectedType) {
    super("Missing property: " + property, property);
    this.name = "PropertyRequiredError";
    this.expectedType = expectedType;
  }
}

export default PropertyRequiredError;
