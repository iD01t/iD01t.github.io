import { Router } from "express";
import { db, now, uid } from "../db.js";
import { requireApiKey } from "../auth/verify.js";
import { z } from "zod";
const r = Router();

const Product = z.object({
  kind: z.enum(['ebook','music','game']),
  slug: z.string().min(3),
  title: z.string().min(1),
  description: z.string().optional(),
  price_cents: z.number().int().positive(),
  currency: z.string().default('CAD'),
  file_url: z.string().url().optional(),
  cover_url: z.string().url().optional()
});

// PUBLIC list & detail
r.get("/", (_req, res) => {
  res.json({ items: db.prepare("SELECT * FROM products ORDER BY created_at DESC").all() });
});
r.get("/:slug", (req, res) => {
  const p = db.prepare("SELECT * FROM products WHERE slug=?").get(req.params.slug);
  if (!p) return res.status(404).json({ error: "Not found" });
  res.json(p);
});

// ADMIN create/update (protect later with your own admin auth)
r.post("/", (req, res) => {
  const b = Product.parse(req.body);
  const id = uid();
  db.prepare(`INSERT INTO products(id,kind,slug,title,description,price_cents,currency,file_url,cover_url,created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?)`).run(id, b.kind, b.slug, b.title, b.description ?? null, b.price_cents, b.currency, b.file_url ?? null, b.cover_url ?? null, now());
  res.status(201).json({ id, ...b });
});

r.patch("/:id", (req, res) => {
  const p = db.prepare("SELECT * FROM products WHERE id=?").get(req.params.id);
  if (!p) return res.status(404).send();
  const fields = Product.partial().parse(req.body);
  const updated = { ...p, ...fields };
  db.prepare(`UPDATE products SET kind=?,slug=?,title=?,description=?,price_cents=?,currency=?,file_url=?,cover_url=? WHERE id=?`)
    .run(updated.kind, updated.slug, updated.title, updated.description, updated.price_cents, updated.currency, updated.file_url, updated.cover_url, p.id);
  res.json(updated);
});

// AUTHENTICATED (API key) – for partner apps to fetch catalog
r.get("/auth/list/all", requireApiKey, (_req, res) => {
  res.json({ items: db.prepare("SELECT * FROM products").all() });
});

export default r;