---
id: US-AUTH-002
title: User can log in with credentials
description: Registered users can authenticate using their email and password
parent_prd: PRD-USER-AUTH
cards:
  - CARD-AUTH-002
status: backlog
acceptance_criteria:
  - User can enter email and password
  - Valid credentials return JWT token
  - Invalid credentials show error message
  - Account lockout after 5 failed attempts
---

# Story: User Login

## User Story

**As a** registered user
**I want to** log in with my credentials
**So that** I can access my account securely

## Acceptance Criteria

- [ ] Email/password form validation
- [ ] JWT token generation on success
- [ ] Clear error messages for failures
- [ ] Rate limiting (5 attempts, then lockout)

## Technical Notes

- JWT expires in 7 days
- Store refresh token in httpOnly cookie
- Log all login attempts for security

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-03-17 | Claude | Created from PRD-USER-AUTH |
