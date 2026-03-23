---
id: CARD-AUTH-002
title: Implement login API endpoint
description: POST /auth/login endpoint for user authentication
parent_story: US-AUTH-002
parent_prd: PRD-USER-AUTH
status: backlog
priority: high
estimate: 3h
---

# Card: Login API

## Task

Implement `POST /auth/login` endpoint.

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
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expiresIn": 604800
}
```

### Response (Error)
```json
{
  "error": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect"
}
```

## Implementation Checklist

- [ ] Create route handler
- [ ] Find user by email
- [ ] Compare password hash
- [ ] Generate JWT token
- [ ] Set refresh token cookie
- [ ] Log login attempt
- [ ] Handle rate limiting

## Files to Create/Modify

- `app/api/auth/login/route.ts`
- `lib/jwt.ts`
- `lib/rate-limiter.ts`

## Testing

- [ ] Unit tests for JWT generation
- [ ] Integration test for login flow
- [ ] Test rate limiting

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-03-17 | Claude | Created from US-AUTH-002 |
