import Database from "better-sqlite3";
import crypto from "crypto";

export const db = new Database(process.env.DB_PATH || "id01t.db");
db.pragma("journal_mode = WAL");

// USERS
db.prepare(`
CREATE TABLE IF NOT EXISTS users(
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TEXT NOT NULL
);`).run();

// TOKENS (hashed)
db.prepare(`
CREATE TABLE IF NOT EXISTS api_tokens(
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);`).run();

// PRODUCTS (union table with kind)
db.prepare(`
CREATE TABLE IF NOT EXISTS products(
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK(kind IN ('ebook','music','game')),
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  price_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CAD',
  file_url TEXT,            -- private storage url
  cover_url TEXT,
  created_at TEXT NOT NULL
);`).run();

// ORDERS
db.prepare(`
CREATE TABLE IF NOT EXISTS orders(
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CAD',
  status TEXT NOT NULL CHECK(status IN ('pending','paid','failed','refunded')),
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);`).run();

// ORDER ITEMS
db.prepare(`
CREATE TABLE IF NOT EXISTS order_items(
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  unit_cents INTEGER NOT NULL,
  qty INTEGER NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY(product_id) REFERENCES products(id)
);`).run();

// LICENSES / DOWNLOADS
db.prepare(`
CREATE TABLE IF NOT EXISTS licenses(
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  order_id TEXT,
  key TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(product_id) REFERENCES products(id)
);`).run();

export function hashToken(token: string) {
  return crypto.createHash("sha256").update(token).digest("hex");
}
export const now = () => new Date().toISOString();
export const uid = () => crypto.randomUUID();