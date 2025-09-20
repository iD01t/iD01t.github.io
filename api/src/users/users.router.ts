import { Router } from "express";
import { db, now, uid } from "../db.js";
import { z } from "zod";
const r = Router();

// Create a user (your admin/session layer should call this)
r.post("/", (req, res) => {
  const body = z.object({ email: z.string().email(), name: z.string().optional() }).parse(req.body);
  const id = uid();
  db.prepare("INSERT INTO users(id,email,name,created_at) VALUES (?,?,?,?)")
    .run(id, body.email, body.name ?? null, now());
  res.status(201).json({ id, ...body });
});

r.get("/", (_req, res) => {
  res.json({ users: db.prepare("SELECT id,email,name,created_at FROM users ORDER BY created_at DESC").all() });
});

export default r;