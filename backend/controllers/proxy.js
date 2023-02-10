import proxy_t from "../objects/proxy.js";
import { create_proxy as cp } from "../services/proxy.js";
import { check_permission } from "../services/token.js";

export async function create_proxy({ body, token }) {
  if (!check_permission(token, "proxy_create")) return;
  const body_proxy = { ...proxy_t, ...body };
  await cp(body_proxy);
}
