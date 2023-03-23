class HeaderError extends Error {
  constructor(message, header) {
    super(message);
    this.name = "HeaderError";
    this.header = header;
  }
}

export default HeaderError;
