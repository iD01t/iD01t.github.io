import { Router } from "express";
import { db, uid, now } from "../db.js";
import crypto from "crypto";
const r = Router();

/**
 * POST /v1/payments/:orderId/capture
 * Body: { provider: 'manual' | 'stripe', payload?: any }
 * For now, mark paid and mint licenses for each item.
 */
r.post("/:orderId/capture", (req, res) => {
  const order = db.prepare("SELECT * FROM orders WHERE id=?").get(req.params.orderId);
  if (!order) return res.status(404).json({ error: "Order not found" });
  if (order.status === "paid") return res.json(order);

  // mark paid
  db.prepare("UPDATE orders SET status='paid' WHERE id=?").run(order.id);

  // create licenses
  const items = db.prepare("SELECT product_id, qty FROM order_items WHERE order_id=?").all(order.id);
  for (const it of items) {
    for (let i = 0; i < it.qty; i++) {
      const key = "lic_" + Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
      db.prepare("INSERT INTO licenses(id,user_id,product_id,order_id,key,created_at) VALUES (?,?,?,?,?,?)")
        .run(uid(), order.user_id, it.product_id, order.id, key, now());
    }
  }

  res.json({ ok: true, status: "paid" });
});

export default r;