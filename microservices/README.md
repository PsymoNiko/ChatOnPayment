# Microservices Architecture

This directory contains the initial microservices scaffold for gradual extraction from the Django monolith.

## Overview

The microservices architecture provides isolated, lightweight services with dedicated responsibilities:

- **Accounts Service**: User authentication, authorization, and JWT key distribution
- **Payments Service**: Payment processing with idempotency support

## Directory Structure

```
microservices/
├── accounts/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── tests/
│   │   └── test_health.py   # Pytest tests
│   ├── Dockerfile
│   └── requirements.txt
└── payments/
    ├── app/
    │   └── main.py          # FastAPI application
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
