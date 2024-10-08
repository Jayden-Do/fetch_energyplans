# Energy Plans in Australia API

## Overview
This repository provides an API to fetch energy plans from different retailers in Australia using the Fiskil API.

## Workflow

### 1. Get Access Token
- Obtain an access token using your `client_id` and `client_secret` (these can be found in your Fiskil account).
  
### 2. Fetch Plans by Retailer
- Use the access token to fetch all available plans for a specific retailer by providing the `retailer_id` (e.g., `origin`, `agl`, etc.).

### 3. Fetch Plan Details
- With the `plan_id` retrieved from the previous response, fetch the detailed plan information.
- Ensure you continue to use the access token for authentication.

## Authentication
- The access token should be included in the request headers as a Bearer token for authentication.

## Example Requests

### Get Access Token
```bash
POST /auth/token
Headers: 
  Content-Type: application/x-www-form-urlencoded
Body: 
  client_id=<your_client_id>
  client_secret=<your_client_secret>
```
### Fetch Plans for a Retailer
```bash
GET /plans?retailer_id=<retailer_id>
Headers: 
  Authorization: Bearer <access_token>
```
### Fetch Plan Details
```bash
GET /plans/<plan_id>
Headers: 
  Authorization: Bearer <access_token>
```

## Notes
- Make sure to handle any errors when making requests to the API.
- Keep your `client_id` and `client_secret` secure.

