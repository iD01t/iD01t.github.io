import type { Request, Response, NextFunction } from "express";

export const notFound = (_req: Request, res: Response) => 
  res.status(404).json({ error: "Not Found" });

export const onError = (err: any, _req: Request, res: Response, _next: NextFunction) => {
  console.error(err);
  res.status(500).json({ error: "Internal Server Error" });
};