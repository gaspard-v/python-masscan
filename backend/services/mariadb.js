import { createPool } from "mariadb";
import * as dotenv from "dotenv";

dotenv.config();
const database = createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  port: process.env.DB_PORT || 3306,
  connectionLimit: 100,
});

export default database;
