from fastapi import HTTPException, status

UserAlreadyExcist = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already registered"
)

IncorrectUserEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect user email or password"
)

AccessTokenIsNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token is not found"
)

InccorrectJWTTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is not a JWT token"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is not valid now"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token does not point to user"
)

InvalidSMSCodeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неправильный смс код!"
)