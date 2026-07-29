from passlib.context import CryptContext


class PasswordService:
    """
    Servicio encargado del hash y validación de contraseñas.
    """

    _pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Genera el hash de una contraseña.
        """
        return cls._pwd_context.hash(password)

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        """
        Verifica una contraseña contra su hash.
        """
        return cls._pwd_context.verify(
            plain_password,
            password_hash,
        )