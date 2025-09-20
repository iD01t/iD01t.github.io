import { Router } from "express";
import { db, now, uid, hashToken } from "../db.js";
import { z } from "zod";
import crypto from "crypto";
const r = Router();

// Create token (requires X-User-Id header for now)
r.post("/", (req, res) => {
  const userId = req.header("X-User-Id");
  if (!userId) return res.status(400).json({ error: "Missing X-User-Id header" });
  
  const body = z.object({ name: z.string().min(1) }).parse(req.body);
  const id = uid();
  const key = "sk_live_" + crypto.randomBytes(32).toString("hex");
  const hash = hashToken(key);
  
  db.prepare("INSERT INTO api_tokens(id,user_id,name,hash,created_at) VALUES (?,?,?,?,?)")
    .run(id, userId, body.name, hash, now());
  
  res.status(201).json({ id, name: body.name, created_at: now(), key });
});

// List tokens for user
r.get("/", (req, res) => {
  const userId = req.header("X-User-Id");
  if (!userId) return res.status(400).json({ error: "Missing X-User-Id header" });
  
  const tokens = db.prepare("SELECT id,name,created_at FROM api_tokens WHERE user_id=? ORDER BY created_at DESC")
    .all(userId);
  res.json({ tokens });
});

// Revoke token
r.delete("/:id", (req, res) => {
  const userId = req.header("X-User-Id");
  if (!userId) return res.status(400).json({ error: "Missing X-User-Id header" });
  
  const result = db.prepare("DELETE FROM api_tokens WHERE id=? AND user_id=?")
    .run(req.params.id, userId);
  
  if (result.changes === 0) return res.status(404).json({ error: "Token not found" });
  res.json({ ok: true });
});

export default r;