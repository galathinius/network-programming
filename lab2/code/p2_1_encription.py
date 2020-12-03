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


# class Connection:
#     def __init__(self, keys):
#         self.priv_key = keys
#         self.pub_key = keys.publickey()
#         self.client_key = None


# conn = Connection(create_keys())

# ecripted = encrypt('hello', conn.pub_key)
# print(dir(ecripted))
# print('\n\n')
# # print(dir(str(ecripted)))
# # print(ecripted == str(ecripted).encode)
# # magiked = bytes(str(ecripted))
# decripted = decrypt(ecripted, conn.priv_key)

# print(decripted)

# def chunks(lst, n):
#     """Yield successive n-sized chunks from lst."""
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]
# whole = b''
# # print(len(chunks(ecripted, 10)))
# for ch in chunks(ecripted, 10):
#     print(ch)
#     whole += ch

# print(decrypt(whole, conn.priv_key))