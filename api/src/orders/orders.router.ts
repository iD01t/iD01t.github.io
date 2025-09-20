import { Router } from "express";
import { db, now, uid } from "../db.js";
import { requireApiKey } from "../auth/verify.js";
import { z } from "zod";
const r = Router();

const CreateOrder = z.object({
  items: z.array(z.object({ product_id: z.string(), qty: z.number().int().positive() })).min(1),
  currency: z.string().default('CAD')
});

// Create order (requires API key = identifies customer app/user)
r.post("/", requireApiKey, (req, res) => {
  const { userId } = (req as any).auth;
  const body = CreateOrder.parse(req.body);

  // price lookup
  const products = body.items.map(i => ({
    ...i,
    price: db.prepare("SELECT price_cents FROM products WHERE id=?").get(i.product_id)?.price_cents
  }));
  if (products.some(p => !p.price)) return res.status(400).json({ error: "Invalid product" });

  const amount = products.reduce((sum, p) => sum + (p.price * p.qty), 0);
  const orderId = uid();

  db.prepare("INSERT INTO orders(id,user_id,amount_cents,currency,status,created_at) VALUES (?,?,?,?,?,?)")
    .run(orderId, userId, amount, body.currency, "pending", now());

  for (const p of products) {
    db.prepare("INSERT INTO order_items(id,order_id,product_id,unit_cents,qty) VALUES (?,?,?,?,?)")
      .run(uid(), orderId, p.product_id, p.price, p.qty);
  }

  res.status(201).json({ id: orderId, amount_cents: amount, currency: body.currency, status: "pending" });
});

// Get order (auth)
r.get("/:id", requireApiKey, (req, res) => {
  const o = db.prepare("SELECT * FROM orders WHERE id=?").get(req.params.id);
  if (!o) return res.status(404).send();
  const items = db.prepare("SELECT * FROM order_items WHERE order_id=?").all(req.params.id);
  res.json({ ...o, items });
});

export default r;