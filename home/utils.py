# utils.py
import base64
from crypto.Cipher import AES
from crypto.Util.Padding import pad, unpad
import hashlib
import os


ENCRYPTION_KEY = 'd0a7e7997b6d5fcd55f4b5c32611b87cd923e88837b63bf2941ef819dc8ca282'

def encrypt(data):
    key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    encoded_data = base64.b64encode(encrypted_data).decode('utf-8') + '|' + base64.b64encode(iv).decode('utf-8')
    return encoded_data

def decrypt(encoded_data):
    key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
    encoded_data, iv = encoded_data.split('|')
    encrypted_data = base64.b64decode(encoded_data)
    iv = base64.b64decode(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')



# USERNAME_MAX_LENGTH = 100
# DISPLAY_NAME_MAX_LENGTH = 20


# def validate_username(username):
#     if not isinstance(username, six.string_types):
#         return False

#     if len(username) > USERNAME_MAX_LENGTH:
#         return False

#     if not username.isalnum():
#         return False

#     if not username.lower().startswith("cpe"):
#         return False

#     return True


# def validate_display_name(display_name):
#     if not isinstance(display_name, six.string_types):
#         return False

#     if len(display_name) > DISPLAY_NAME_MAX_LENGTH:
#         return False

#     if not display_name.replace(' ', '').isalnum():
#         return False

#     return True


# # if User.objects.filter(username=username).exists():
# #             error = 'Student already exists.'
# #             return render(request, 'register.html', context = {'page_title': "Register", 'error': error})
