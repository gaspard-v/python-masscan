import { proxy_t, default_proxy } from "../objects/proxy.js";
import { create_proxy as cp, get_proxies as gp } from "../services/proxy.js";

export async function create_proxy({ body }) {
  const constructed_proxy = { ...default_proxy, ...body };
  return await cp(constructed_proxy);
}

export async function get_proxies({ number }) {
  const result = await gp({ number: number });
  let result_string = "";
  result.forEach(({ address, port }) => {
    result_string += `(http)${address}:${port}\n`; // TODO, intergrer le protocole dans la base de donnée
  });
  return result_string;
}
