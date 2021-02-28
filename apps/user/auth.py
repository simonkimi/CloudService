from django.contrib.auth.hashers import BasePasswordHasher


class EmptyPasswordHasher(BasePasswordHasher):
    algorithm = "empty"

    def encode(self, password, salt):
        return f'{self.algorithm}${password}'

    def verify(self, password: str, encoded):
        return encoded.split("$", 1)[1] == password

    def safe_summary(self, encoded):
        return {
            'algorithm': encoded.split("$", 1)
        }
