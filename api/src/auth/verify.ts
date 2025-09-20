import type { Request, Response, NextFunction } from "express";
import { db, hashToken } from "../db.js";

export function requireApiKey(req: Request, res: Response, next: NextFunction) {
  const key = (req.header("Authorization") || "").replace(/^Bearer\s+/i, "");
  if (!key) return res.status(401).json({ error: "Missing API key" });

  const row = db.prepare("SELECT id, user_id FROM api_tokens WHERE hash=?").get(hashToken(key));
  if (!row) return res.status(403).json({ error: "Invalid API key" });

  (req as any).auth = { tokenId: row.id, userId: row.user_id };
  next();
}