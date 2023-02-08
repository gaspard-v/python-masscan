import database from "./mariadb.js";

export async function create_proxy({
  address,
  port,
  ip_type,
  methodes,
  scan_date,
  commentaire,
}) {
  const conn = await database.getConnection();
  const result = await conn.query("CALL add_proxy(?,?,?,?,?,?)", [
    address,
    port,
    ip_type,
    methodes,
    scan_date,
    commentaire,
  ]);
  return result;
}
