import TokenError from "./TokenError.js";

class TokenPermissionError extends TokenError {
  constructor(token, permission) {
    super(
      "you are not authorized to perform this action with the given token",
      token
    );
    this.permission = permission;
  }
}

export default TokenPermissionError;
