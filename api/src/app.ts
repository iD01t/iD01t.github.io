import "dotenv/config";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import rateLimit from "express-rate-limit";
import { notFound, onError } from "./utils/errors.js";

import users from "./users/users.router.js";
import tokens from "./tokens/tokens.router.js";
import products from "./products/products.router.js";
import orders from "./orders/orders.router.js";
import payments from "./payments/payments.router.js";
import licenses from "./licenses/licenses.router.js";

const app = express();
app.set("trust proxy", 1);
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN?.split(",") || "*" }));
app.use(express.json({ limit: "1mb" }));
app.use(morgan("dev"));
app.use(rateLimit({ windowMs: 60_000, limit: 120 }));

app.get("/v1/health", (_req, res) => res.json({ ok: true }));

app.use("/v1/users", users);
app.use("/v1/tokens", tokens);
app.use("/v1/products", products);
app.use("/v1/orders", orders);
app.use("/v1/payments", payments);
app.use("/v1/licenses", licenses);

app.use(notFound);
app.use(onError);

const port = Number(process.env.PORT || 3001);
app.listen(port, () => console.log(`iD01t API listening on :${port}`));