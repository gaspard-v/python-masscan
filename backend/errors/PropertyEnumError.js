import PropertyError from "./propertyError.js";

class PropertyEnumError extends PropertyError {
  constructor(property, allowedValues) {
    super(
      `Property ${property} should be one of ${allowedValues.join(", ")}`,
      property
    );
    this.name = "PropertyEnumError";
    this.allowedValues = allowedValues;
  }
}

export default PropertyEnumError;
