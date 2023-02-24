from passlib.context import CryptContext

pwd_context = CryptContext(schemes='bcrypt', deprecated="auto")
        #using bcrypt hashing algorithm
        #deprecated="auto" will provide us with legacy support


#hasher to get and verify hashed password
class Hasher:

    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)


    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)
