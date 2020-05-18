from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(account, secret_key, security_pwd_salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(account, salt=security_pwd_salt)


def confirm_token(token, secret_key, security_pwd_salt, expiration=1800):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        account = serializer.loads(
            token,
            salt=security_pwd_salt,
            max_age=expiration
        )
    except:
        return False
    return account
