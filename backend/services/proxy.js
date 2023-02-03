import database from "./mariadb.js";

export async function create_proxy({
  address,
  port,
  ip_type,
  methodes,
  scan_date,
  commentaire,
  token,
}) {
  return database
    .getConnection()
    .then((conn) =>
      conn.query("CALL add_proxy(?,?,?,?,?,?)", [
        address,
        port,
        ip_type,
        methodes,
        scan_date,
        commentaire,
      ])
    )
    .then((result) => result);
}
