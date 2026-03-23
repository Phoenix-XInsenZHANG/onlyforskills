# User Authentication Design

## Problem

Users need to securely log in to access their organization's data. Currently there's no authentication system.

## Solution

Implement email/password authentication with JWT tokens, plus OAuth providers (Google, GitHub).

## Implementation

### Approach A: Email/Password Only (Recommended)
- Simple to implement
- Users manage credentials
- Password reset via email

### Approach B: OAuth Only
- No password management
- Delegated to providers
- More complex setup

### Approach C: Hybrid
- Both email/password and OAuth
- Most flexible but most complex

## Success Criteria

- [ ] Users can register with email/password
- [ ] Users can log in and receive JWT
- [ ] Session persists for 7 days
- [ ] OAuth login works for Google/GitHub

## Technical Details

### API Endpoints
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- GET /auth/oauth/google
- GET /auth/oauth/github

### Error Handling
- Invalid credentials: 401
- Account locked: 423
- Rate limited: 429

## Stories

1. User can register with email
2. User can log in with credentials
3. User can log in with OAuth
4. User can reset password
