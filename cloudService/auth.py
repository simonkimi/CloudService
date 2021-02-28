from django.contrib.auth.hashers import BasePasswordHasher


class EmptyPasswordHasher(BasePasswordHasher):
    algorithm = "empty"

    def encode(self, password, salt):
        return password

    def verify(self, password: str, encoded):
        return encoded == password

    def safe_summary(self, encoded):
        return {
            'algorithm': self.algorithm
        }
