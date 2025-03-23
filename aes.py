# from remote_transmit import send_remote_file, retrieve_remote_files

# from remote_config_entries import remote_configs
# '''
# class RemoteConfig:
#     def __init__(self, hostname, username, password, remote_path, index, port=22, nonce=0): # Added port, defaults to 22
#         self.hostname = hostname
#         self.username = username
#         self.password = password
#         self.remote_path = remote_path
#         self.port = port
#         self.nonce = nonce
#         self.index = index
# '''




from Crypto.Cipher import AES
import os
import struct

def encrypt_tuple(data_tuple, key):
    """
    Wrapper for AES-GCM that runs on a secret-share tuple

    Args:
        data_tuple (tuple): The secret share
        key (256 bit int): The secret encryption key

    Returns:
        nonce, ciphertext, tag (bytes): The result of AES-GCM is the encrypted ciphertext, the public random element (nonce) and the authentication tag
    """
    # Convert the tuple to a byte string
    data_bytes = struct.pack(f'>{len(data_tuple)}i', *data_tuple)
    # Generate a random nonce
    nonce = os.urandom(16)
    # Create the cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
    # Return the nonce, ciphertext, and tag
    return nonce, ciphertext, tag

def decrypt_tuple(nonce, ciphertext, tag, key):
    # Create the cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    # Decrypt the data
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    # Convert the byte string back to a tuple
    data_tuple = struct.unpack(f'>{len(plaintext) // 4}i', plaintext)
    # Return the tuple
    return data_tuple

# Example usage
key = os.urandom(32)  # Generate a random 256-bit key
data_tuple = (1, 2, 3, 4, 5)

# Encrypt the tuple
nonce, ciphertext, tag = encrypt_tuple(data_tuple, key)

print(nonce)
print(ciphertext)
print(tag)

# Decrypt the tuple
decrypted_tuple = decrypt_tuple(nonce, ciphertext, tag, key)

print("Original tuple:", data_tuple)
print("Decrypted tuple:", decrypted_tuple)