# Microservices Architecture

This directory contains the initial microservices scaffold for gradual extraction from the Django monolith.

## Overview

The microservices architecture provides isolated, lightweight services with dedicated responsibilities:

- **Accounts Service**: User authentication, authorization, account balance management, and transactions
- **Payments Service**: Payment processing with idempotency support
- **Chat Service**: Real-time messaging via WebSocket connections
- **Basement Service**: File upload, thumbnail generation, and category management
- **Resume Service**: Resume creation, management, and retrieval

## Directory Structure

```
microservices/
├── accounts/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── tests/
│   │   ├── test_health.py   # Health check tests
│   │   └── test_accounts.py # User and account tests
│   ├── Dockerfile
│   └── requirements.txt
├── payments/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── chat/
│   ├── app/
│   │   └── main.py          # FastAPI application with WebSocket support
│   ├── tests/
│   │   └── test_chat.py     # Chat and WebSocket tests
│   ├── Dockerfile
│   └── requirements.txt
└── basement/
    ├── app/
    │   └── main.py          # FastAPI application
    ├── tests/
    │   └── test_basement.py # File and category tests
    ├── Dockerfile
    └── requirements.txt
└── resume/
    ├── app/
    │   └── main.py          # FastAPI application
    ├── tests/
    │   └── test_resume.py   # Resume tests
    ├── Dockerfile
    └── requirements.txt
```

## Running the Microservices

### Using Docker Compose (Recommended)

Start all microservices with the gateway:

```bash
docker compose -f docker-compose.micro.yml up --build
```

The services will be available at:
- Gateway: http://localhost:8080
- Accounts: http://localhost:8080/accounts/
- Payments: http://localhost:8080/payments/
- Chat: http://localhost:8080/chat/
- Basement: http://localhost:8080/basement/
- Resume: http://localhost:8080/resume/

### Stopping Services

```bash
docker compose -f docker-compose.micro.yml down
```

## API Endpoints

### Accounts Service

#### Health & Readiness
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness probe

#### Authentication (Stubs)
- `GET /.well-known/jwks.json` - JWKS endpoint (returns empty keys array)
- `GET /users/me` - Current user information (stub)

#### User Management
- `POST /users` - Create a new user
  - Request body: `{"phone_number": "1234567890", "password": "pass", "date_of_birth": "1990-01-01"}`
  - Returns user details including auto-generated account
- `GET /users/{user_id}` - Get user by ID

#### Account Management
- `GET /accounts/user/{user_id}` - Get account for a user
- `POST /transactions` - Create a transaction between accounts
  - Request body: `{"sender_id": "acc-id-1", "receiver_id": "acc-id-2", "amount": "100.00"}`
- `GET /transactions/{transaction_id}` - Get transaction details

### Payments Service

#### Health & Readiness
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness probe

#### Payments
- `POST /payments` - Create payment (requires `Idempotency-Key` header)
  - Returns 202 Accepted
  - Example request:
    ```bash
    curl -X POST http://localhost:8080/payments/payments \
      -H "Content-Type: application/json" \
      -H "Idempotency-Key: unique-key-123" \
      -d '{"amount": 100.00, "currency": "USD", "description": "Test payment"}'
    ```

### Chat Service

#### Health & Readiness
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness probe

#### Chat & WebSocket
- `WS /ws/{room_name}` - WebSocket endpoint for real-time chat
  - Connect to a room and send/receive messages
  - Message format: `{"message": "text", "phone_number": "user", "avatar": "url"}`
  - Example:
    ```javascript
    const ws = new WebSocket('ws://localhost:8080/chat/ws/test-room');
    ws.send(JSON.stringify({message: "Hello!", phone_number: "123", avatar: "url"}));
    ```
- `GET /rooms/{room_name}/info` - Get room information (active connections count)

### Basement Service

#### Health & Readiness
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness probe

#### File Management
- `POST /files/upload` - Upload a file with optional thumbnail generation
  - Multipart form data with file field
  - Optional: `file_tags`, `bucket_name` (default: "chat-bucket")
  - Automatically creates thumbnails for images (except SVG)
- `GET /files/{file_id}` - Get file information

#### Category Management
- `POST /categories` - Create a new category
  - Request body: `{"title": "Category Name", "parent_id": "optional-parent-id"}`
  - Auto-generates slug and calculates level
- `GET /categories/{category_id}` - Get category by ID
- `GET /categories` - List all categories

### Resume Service

#### Health & Readiness
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness probe

#### Resume Management
- `POST /resumes` - Create a new resume
  - Request body: `{"user_id": "user-123", "title": "Software Engineer", "summary": "Experienced developer", "skills": ["Python", "FastAPI"], "experience": "5 years", "education": "BS in CS"}`
  - Returns resume details with auto-generated ID
- `GET /resumes/{resume_id}` - Get resume by ID
- `GET /resumes/user/{user_id}` - Get resume by user ID
- `PUT /resumes/{resume_id}` - Update a resume
  - Request body: `{"title": "Senior Software Engineer", "skills": ["Python", "FastAPI", "Docker"]}`
- `DELETE /resumes/{resume_id}` - Delete a resume
- `GET /resumes` - List all resumes

## Testing

### Running Tests for Accounts Service

Inside the container:
```bash
docker exec accounts-service python -m pytest tests/test_health.py -v
```

All tests should pass:
- ✅ test_health_endpoint
- ✅ test_readiness_endpoint
- ✅ test_jwks_endpoint
- ✅ test_users_me_stub

### Running Tests for Resume Service

Inside the container:
```bash
docker exec resume-service python -m pytest tests/test_resume.py -v
```

All tests should pass:
- ✅ test_health_endpoint
- ✅ test_readiness_endpoint
- ✅ test_create_resume
- ✅ test_get_resume
- ✅ test_update_resume
- ✅ test_delete_resume
- ✅ test_list_resumes

## Architecture Notes

### Current State (Stubs)
- JWKS endpoint returns empty keys array (JWT issuance not implemented)
- User endpoint returns stub data (no real authentication)
- Payments endpoint accepts requests but doesn't process them (no persistence)
- No event publishing or outbox pattern

### Isolation from Monolith
- Independent docker-compose.micro.yml (isolated from heavy observability stack)
- No dependencies on existing Django services
- Separate network namespace

## Future Enhancements

The following features are planned for future PRs:

### Security & Authentication
- [ ] Implement real JWT issuance in Accounts service
- [ ] Add JWT verification middleware
- [ ] Populate JWKS endpoint with real public keys
- [ ] Add user authentication and authorization

### Payments
- [ ] Implement payment persistence (database)
- [ ] Add real idempotency logic
- [ ] Implement payment processing workflow
- [ ] Add event publishing for payment state changes

### Observability
- [ ] Add structured JSON logging
- [ ] Implement correlation IDs across services
- [ ] Add distributed tracing (OpenTelemetry)
- [ ] Add metrics collection (Prometheus)
- [ ] Add health check dependencies

### Infrastructure
- [ ] Pin all dependencies with version constraints
- [ ] Multi-stage Docker builds
- [ ] Run containers as non-root user
- [ ] Add resource limits
- [ ] Implement outbox pattern for events
- [ ] Add CI/CD pipeline (lint, test, security scan, build, push)

### Integration
- [ ] Add service-to-service authentication
- [ ] Implement circuit breakers
- [ ] Add rate limiting
- [ ] Add API versioning

## Development Guidelines

1. **Keep it simple**: These are stubs for validation, not production-ready services
2. **Test first**: Add tests before implementing features
3. **Security**: Run security scans before committing
4. **Documentation**: Update this README when adding features
5. **Isolation**: Don't modify monolith code

## Troubleshooting

### Services won't start
Check Docker logs:
```bash
docker compose -f docker-compose.micro.yml logs
```

### Health checks failing
Verify services are responding:
```bash
curl http://localhost:8080/accounts/healthz
curl http://localhost:8080/payments/healthz
```

### Tests failing
Run tests with verbose output:
```bash
docker exec accounts-service python -m pytest tests/ -v --tb=short
```
