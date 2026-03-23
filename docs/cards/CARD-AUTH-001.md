---
id: CARD-AUTH-001
title: Implement registration API endpoint
description: POST /auth/register endpoint for user registration
parent_story: US-AUTH-001
parent_prd: PRD-USER-AUTH
status: backlog
priority: high
estimate: 2h
---

# Card: Registration API

## Task

Implement `POST /auth/register` endpoint.

## API Contract

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Response (Success)
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

### Response (Error)
```json
{
  "error": "EMAIL_EXISTS",
  "message": "An account with this email already exists"
}
```

## Implementation Checklist

- [ ] Create route handler
- [ ] Validate email format
- [ ] Check password length (8+)
- [ ] Hash password with bcrypt
- [ ] Check for duplicate email
- [ ] Insert user into database
- [ ] Send confirmation email
- [ ] Return appropriate response

## Files to Create/Modify

- `app/api/auth/register/route.ts`
- `lib/validators/auth.ts`
- `lib/services/auth-service.ts`

## Testing

- [ ] Unit tests for validation
- [ ] Integration test for endpoint
- [ ] Test duplicate email handling

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-03-17 | Claude | Created from US-AUTH-001 |
