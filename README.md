# API OL6 API Collection

## Overview
This collection contains various API endpoints for the `API OL6`. It is designed to be used with Flask in Python. Below are examples of some of the API calls available in this collection.

### Endpoints

#### Login
- **Method**: POST
- **URL**: `http://127.0.0.1:5000/api/login`
- **Body**:
```json
{
    "email": "example@example.br",
    "password": "12345678"
}
```

#### Create User
- **Method**: POST
- **URL**: `http://127.0.0.1:5000/api/users`
- **Body**:
```json
{
    "email": "example@example.br",
    "password": "12345678"
}
```

#### Get User
- **Method**: GET
- **URL**: `http://127.0.0.1:5000/api/users/65786e1193f21fd40cb60b20`
- **Body**:
```json

```

## Usage
To use these APIs, import the collection into Postman and make the necessary requests to the specified endpoints.
