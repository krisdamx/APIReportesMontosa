from app.services.jwt_service import JwtService

token = JwtService.create_access_token(
    user_id=1,
    username="admin",
)

print("TOKEN")
print(token)

print()

payload = JwtService.decode_token(token)

print("PAYLOAD")
print(payload)