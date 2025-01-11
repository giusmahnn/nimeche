# import secrets
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# random_secret_key = secrets.token_urlsafe(64)
# print(random_secret_key)  # Copy and use this as your JWT_SECRET_KEY



def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "is_staff": user.is_staff,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
    }

    token=jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
    except jwt.InvalidSignatureError:
        return "Invalid signature. Please log in again."
    except jwt.DecodeError:
        return "Error decoding signature. Please log in again."
    except Exception as e:
        return str(e)