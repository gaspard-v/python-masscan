class TokenError extends Error {
  constructor(message, token) {
    super(message);
    this.name = "TokenError";
    this.token = token;
  }
}

export default TokenError;
