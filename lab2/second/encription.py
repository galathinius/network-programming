# class Connection:
#     def __init__(self, keys):
#         self.priv_key = keys
#         self.pub_key = keys.publickey()
#         self.client_key = None


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def create_keys():
    private_key = RSA.generate(2048)
    return private_key

def get_key_from_string(key):
    return RSA.importKey(key)

def decrypt(mess, key):
    rsa_private_key = PKCS1_OAEP.new(key)
    decrypted_info = rsa_private_key.decrypt(mess)
    return decrypted_info.decode("utf-8")

def encrypt(mess, key):
    rsa_public_key = PKCS1_OAEP.new(key)
    mess = mess.encode('utf-8')
    enc_data = rsa_public_key.encrypt(mess)
    return enc_data

# conn = Connection(create_keys())

# ecripted = encrypt('hello', conn)
# print(ecripted)
# decripted = decrypt(ecripted, conn)

# print(decripted)