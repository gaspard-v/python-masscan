import proxy_t from "../objects/proxy.js";
import { create_proxy as cp } from "../services/proxy.js";

export async function create_proxy(body) {
  const body_proxy = { ...proxy_t, ...body };
  await cp(body_proxy);
}
