from app.services.password_service import PasswordService

password = "123456"

password_hash = PasswordService.hash_password(password)

print("Hash generado:")
print(password_hash)

print()

print("Password correcta:")
print(
    PasswordService.verify_password(
        "123456",
        password_hash,
    )
)

print()

print("Password incorrecta:")
print(
    PasswordService.verify_password(
        "abcdef",
        password_hash,
    )
)