import base64

from django.conf import settings

from cryptography.fernet import Fernet


def encrypt(text: str):
    encrypted_text = Fernet(settings.ENCRYPT_KEY).encrypt(text.encode())
    return base64.urlsafe_b64encode(encrypted_text).decode()


def decrypt(text: str):
    text = base64.urlsafe_b64decode(text)
    return Fernet(settings.ENCRYPT_KEY).decrypt(text).decode()
