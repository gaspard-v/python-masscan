import ValidationError from "./ValidationError";

class PropertyError extends ValidationError {
  constructor(message, property) {
    super(message);
    this.name = "PropertyError";
    this.property = property;
  }
}

export default PropertyError;
