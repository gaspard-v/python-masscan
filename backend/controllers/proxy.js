import { proxy_t, default_proxy } from "../objects/proxy.js";
import { create_proxy as cp } from "../services/proxy.js";

export async function create_proxy({ body }) {
  const constructed_proxy = { ...default_proxy, ...body };
  return await cp(constructed_proxy);
}
