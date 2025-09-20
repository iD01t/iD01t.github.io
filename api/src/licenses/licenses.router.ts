import { Router } from "express";
import { db } from "../db.js";
import { requireApiKey } from "../auth/verify.js";
const r = Router();

// List my licenses
r.get("/", requireApiKey, (req, res) => {
  const { userId } = (req as any).auth;
  const rows = db.prepare(`
    SELECT l.id, l.key, p.title, p.kind, p.cover_url, p.file_url
    FROM licenses l JOIN products p ON p.id=l.product_id
    WHERE l.user_id=? ORDER BY l.created_at DESC
  `).all(userId);
  res.json({ licenses: rows });
});

// Exchange license for a signed download URL (for now return file_url)
r.post("/:id/download", requireApiKey, (req, res) => {
  const { userId } = (req as any).auth;
  const lic = db.prepare("SELECT l.*, p.file_url FROM licenses l JOIN products p ON p.id=l.product_id WHERE l.id=? AND l.user_id=?")
    .get(req.params.id, userId);
  if (!lic) return res.status(404).send();
  // TODO: generate short-lived signed URL from your storage. For now:
  res.json({ url: lic.file_url });
});

export default r;