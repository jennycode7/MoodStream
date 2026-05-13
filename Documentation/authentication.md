# Authentication

This section covers user registration, login, token management, and logout for the MoodStream API.

---

## Register User

Create a new user account.

**Endpoint:**

```http
POST /api/accounts/register/
```

### Request Body

```json
{
  "username": "jennifer",
  "email": "jennifer@example.com",
  "password": "securepassword",
  "preferred_mood": "happy"
}
```

### Field Descriptions

| Field          | Type   | Required | Description                    |
| -------------- | ------ | -------- | ------------------------------ |
| username       | string | ✅        | Unique username                |
| email          | string | ✅        | User email address             |
| password       | string | ✅        | User password                  |
| preferred_mood | string | ✅        | User's default mood preference |

### Response

```json
{
  "message": "User created successfully"
}
```

---

##  Login

Authenticate a user and receive JWT tokens.

**Endpoint:**

```http
POST /api/accounts/login/
```

### Request Body

```json
{
  "username": "jennifer",
  "password": "securepassword"
}
```

### Response

```json
{
  "message": "Login successful",
  "access": "your_access_token",
  "refresh": "your_refresh_token",
  "user": {
    "id": 1,
    "username": "jennifer",
    "email": "jennifer@example.com",
    "preferred_mood": "happy"
  }
}
```

---

## 🔄 Refresh Access Token

Generate a new access token using a refresh token.

**Endpoint:**

```http
POST /api/token/refresh/
```

### Request Body

```json
{
  "refresh": "your_refresh_token"
}
```

### Response

```json
{
  "access": "new_access_token"
}
```

---

## Logout

Invalidate the user's session by blacklisting the refresh token.

**Endpoint:**

```http
POST /api/accounts/logout/
```

### Request Body

```json
{
  "refresh": "your_refresh_token"
}
```

### Description

* This endpoint **blacklists the refresh token**
* After logout, the token can no longer be used to generate new access tokens

### Response

```json
{
  "message": "Logout successful"
}
```

---

## 🔐 Authentication Method

This API uses **JWT (JSON Web Token)** authentication.

### How to Authenticate Requests

Include the access token in request headers:

```http
Authorization: Bearer <your_access_token>
```

---

## Common Errors

### Invalid Credentials

```json
{
  "detail": "Invalid username or password"
}
```

---

### Token Not Valid

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

### Missing Token

```json
{
  "detail": "Authentication credentials were not provided."
}
```
