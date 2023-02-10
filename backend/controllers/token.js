import { get_permission as gp } from "../services/token.js";

export async function get_permission(token) {
  return await gp({ token: token });
}
