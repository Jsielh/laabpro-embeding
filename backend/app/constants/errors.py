HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "NO_CONTENT": 204,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "UNPROCESSABLE_ENTITY": 422,
    "INTERNAL_SERVER_ERROR": 500,
    "SERVICE_UNAVAILABLE": 503,
}

ERROR_TYPES = {
    "VALIDATION": "validation_error",
    "AUTHENTICATION": "authentication_error",
    "AUTHORIZATION": "authorization_error",
    "NOT_FOUND": "not_found_error",
    "SERVER": "server_error",
}

HEADERS = {
    "CONTENT_TYPE": "Content-Type",
    "AUTHORIZATION": "Authorization",
    "APPLICATION_JSON": "application/json",
    "TEXT_EVENT_STREAM": "text/event-stream",
    "CACHE_CONTROL": "Cache-Control",
    "NO_CACHE": "no-cache",
}
