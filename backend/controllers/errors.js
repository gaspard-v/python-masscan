export async function create({ status, message, err }) {
  return {
    status: status,
    message: message,
    details: err,
  };
}
