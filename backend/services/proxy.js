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

export async function get_proxies({ number }) {
  const conn = await database.getConnection();
  let query = "SELECT * FROM proxy ORDER BY update_date DESC";
  if (number) query += ` LIMIT ${number}`;
  return await conn.query(query);
}
