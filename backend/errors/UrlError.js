class UrlError extends Error {
  constructor(message, url) {
    super(message);
    this.name = "UrlError";
    this.url = url;
  }
}

export default UrlError;
