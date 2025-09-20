# iD01t Productions API

A comprehensive REST API for managing eBooks, music, games, users, orders, payments, and digital licenses.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Setup
Copy `.env` and adjust as needed:
```env
PORT=3001
DB_PATH=./id01t.db
CORS_ORIGIN=https://id01t.store,https://www.id01t.store
```

### 3. Run Development Server
```bash
npm run dev
```

The API will be available at `http://localhost:3001`

### 4. Production Build
```bash
npm run build
npm start
```

## API Endpoints

### Health Check
```
GET /v1/health
```

### Users Management
```
POST /v1/users          # Create user
GET  /v1/users          # List users
```

### API Tokens
```
POST   /v1/tokens       # Create token (requires X-User-Id header)
GET    /v1/tokens       # List tokens (requires X-User-Id header)
DELETE /v1/tokens/:id   # Revoke token (requires X-User-Id header)
```

### Products (eBooks, Music, Games)
```
GET    /v1/products                 # Public: List all products
GET    /v1/products/:slug           # Public: Get product by slug
POST   /v1/products                 # Admin: Create product
PATCH  /v1/products/:id             # Admin: Update product
GET    /v1/products/auth/list/all   # Authenticated: Full catalog (requires API key)
```

### Orders
```
POST /v1/orders     # Create order (requires API key)
GET  /v1/orders/:id # Get order details (requires API key)
```

### Payments
```
POST /v1/payments/:orderId/capture  # Capture payment and generate licenses
```

### Licenses & Downloads
```
GET  /v1/licenses              # List my licenses (requires API key)
POST /v1/licenses/:id/download # Get download URL (requires API key)
```

## Database Schema

### Tables
- **users**: User accounts
- **api_tokens**: Hashed API tokens for authentication
- **products**: eBooks, music, games (union table)
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **licenses**: Digital licenses generated after payment

## Usage Examples

### 1. Create a User
```bash
curl -X POST http://localhost:3001/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"John Doe"}'
```

### 2. Create API Token
```bash
curl -X POST http://localhost:3001/v1/tokens \
  -H "Content-Type: application/json" \
  -H "X-User-Id: USER_ID_HERE" \
  -d '{"name":"My CLI Token"}'
```

### 3. Create Product
```bash
curl -X POST http://localhost:3001/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "kind": "ebook",
    "slug": "my-ebook",
    "title": "My Amazing eBook",
    "description": "A great read",
    "price_cents": 1999,
    "currency": "CAD",
    "file_url": "https://storage.example.com/ebook.pdf",
    "cover_url": "https://storage.example.com/cover.jpg"
  }'
```

### 4. Create Order
```bash
curl -X POST http://localhost:3001/v1/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_live_YOUR_API_KEY" \
  -d '{
    "items": [{"product_id": "PRODUCT_ID", "qty": 1}],
    "currency": "CAD"
  }'
```

### 5. Capture Payment
```bash
curl -X POST http://localhost:3001/v1/payments/ORDER_ID/capture \
  -H "Content-Type: application/json" \
  -d '{"provider": "manual"}'
```

### 6. List Licenses
```bash
curl -X GET http://localhost:3001/v1/licenses \
  -H "Authorization: Bearer sk_live_YOUR_API_KEY"
```

## Frontend Integration

To fix the `/usersSettings/tokens` 404 error, create a page that:

1. **Lists tokens**: `GET /v1/tokens` with `X-User-Id` header
2. **Creates tokens**: `POST /v1/tokens` with user ID and token name
3. **Revokes tokens**: `DELETE /v1/tokens/:id` with user ID

Example frontend code:
```javascript
// Create token
const response = await fetch('/api/v1/tokens', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-User-Id': user.id
  },
  body: JSON.stringify({ name: 'My App Token' })
});
const { key } = await response.json(); // Show this once!
```

## Next Steps

1. **Stripe Integration**: Replace payment stub with real Stripe PaymentIntents
2. **File Storage**: Use S3/R2 with signed URLs for secure downloads
3. **Admin Authentication**: Add proper admin middleware for product management
4. **Rate Limiting**: Add per-route rate limits and idempotency keys
5. **Webhooks**: Add webhook endpoints for payment providers

## Architecture

- **Express.js** with TypeScript
- **SQLite** database with WAL mode
- **Zod** for request validation
- **API Key authentication** with hashed tokens
- **Modular router structure** for easy maintenance

## Security Features

- API key authentication
- CORS protection
- Helmet security headers
- Rate limiting
- Input validation with Zod
- Hashed token storage

## Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

The API includes comprehensive error handling, request validation, and follows REST conventions for easy integration with your existing iD01t Productions website.