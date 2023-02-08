import database from "./mariadb.js";

async function check_permission({ token, permission }) {
  const conn = await database.getConnection();
  const result = await conn.query("CALL get_token_permission(?)", [token]);
}
