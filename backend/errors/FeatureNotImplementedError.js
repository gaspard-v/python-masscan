class FeatureNotImplementedError extends Error {
  constructor(message) {
    super(message);
    this.name = "FeatureNotImplementedError";
  }
}

export default FeatureNotImplementedError;
