import proxy_t from "../objects/proxy.js";

export async function create_proxy(body) {
  const body_proxy = { ...proxy_t, ...body };
}
