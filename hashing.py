from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    def bcrypt(password: str):
        return pwd_ctx.hash(password)

    def verify(plain_passwd: str, enc_passwd:str):
        return pwd_ctx.verify(plain_passwd, enc_passwd)