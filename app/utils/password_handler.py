from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Argon2 hasher
ph = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.
    Returns a string containing the hash, salt, and parameters.
    """
    return ph.hash(password)

def verify_password(hashed_password: str, provided_password: str) -> bool:
    """
    Verify a provided password against the stored Argon2 hash.
    Returns True if they match, False otherwise.
    """
    try:
        ph.verify(hashed_password, provided_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Password verification error: {e}")
        return False
