# test_security.py
import sys
sys.path.append('backend')

from backend.src.utils.security import hash_password, verify_password, create_access_token, verify_token

# Test password hashing
password = "mypassword123"
hashed = hash_password(password)
print(f"✅ Password hashed: {hashed[:50]}...")

# Test password verification
is_valid = verify_password(password, hashed)
print(f"✅ Password verification: {is_valid}")

# Test wrong password
is_invalid = verify_password("wrongpassword", hashed)
print(f"✅ Wrong password rejected: {not is_invalid}")

# Test JWT token creation
token = create_access_token({"sub": "123"})
print(f"✅ Access token created: {token[:50]}...")

# Test token verification
payload = verify_token(token, "access")
print(f"✅ Token verified, user_id: {payload.get('sub')}")

print("\n🎉 All security functions working!")