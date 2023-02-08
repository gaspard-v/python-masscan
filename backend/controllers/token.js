import { check_permission as cp } from "../services/token.js";
import permission from "../objects/permission.js";

export async function check_permission(token) {
  await cp({ token: token, permission: permission.proxy_create });
}
