import database from "./mariadb.js";

export async function get_permission({ token }) {
  const conn = await database.getConnection();
  const [result] = await conn.query("CALL get_token_permission(?)", [token]);
  if (conn) await conn.end();
  const result_array = result.map(({ permission }) => permission);
  return result_array;
}

export async function check_permission({ token, permission }) {
  const result = await get_permission({ token: token });
  if (!result.length) return [false, "token does not not exist"];
  if (result.includes(permission)) return [true, ""];
  if (result.includes("all_all")) return [true, ""];
  if (permission.startsWith("proxy_")) {
    return [result.includes("proxy_all"), ""];
  }
  if (permission.startsWith("token_")) {
    return [result.includes("token_all"), ""];
  }
  return [false, "not permitted"];
}
