import PropertyError from "./propertyError.js";

class PropertyTypeError extends PropertyError {
  constructor(property, expectedType) {
    super(`Property ${property} should be a ${expectedType}`, property);
    this.name = "PropertyTypeError";
    this.expectedType = expectedType;
  }
}

export default PropertyTypeError;
