# Regular Python Imports
import os
from Crypto.Hash import SHA3_256
import json
import base64

# Imports from the github repo
from shamir_secret_sharing import split_secret, reconstruct_secret
from aes import encrypt_tuple, decrypt_tuple
from remote_config_entries import remote_configs
from remote_transmit import send_remote_file, retrieve_remote_files

DATABASE_MASTERKEY = 'Database Masterkey string can really be anything, just store it securely'
NUM_HONEST_PARTICIPANTS = 2  # Example threshold (k) formlerly 3
NUM_PARTICIPANTS = 2         # Example number of shares (n) formerly 5

SHAMIR_SECRET = 42
SHAMIR_SEED = int.from_bytes(os.urandom(32), signed=False)

# Setup random nonces for each person (use legitimate random sampling as opposed to a 
# nonlinear shift register such as romu, so that one person having a nonce has no predicting 
# power on another person's nonce)
for config in remote_configs:
    config.nonce = os.urandom(16)

# for config in remote_configs:
#     print(config.nonce)

shares = split_secret(SHAMIR_SECRET, SHAMIR_SEED, NUM_PARTICIPANTS, NUM_HONEST_PARTICIPANTS)

print(shares)

'''
Encryption and Decryption within a single program (tested, it works)
'''

# encrypted_shares = []

# for share in shares:
#     index, yval = share
#     nonce = remote_configs[index - 1].nonce

#     h_obj = SHA3_256.new()
#     hash_input = f"{DATABASE_MASTERKEY} | {nonce.hex()}"
#     h_obj.update(hash_input.encode('utf-8'))
#     key = h_obj.digest()

#     encrypted_shares.append(encrypt_tuple(share, key, nonce))

# print(encrypted_shares)

# decrypted_shares = []

# for index, enc_share in enumerate(encrypted_shares):
#     h_obj = SHA3_256.new()
#     hash_input = f"{DATABASE_MASTERKEY} | {enc_share[0].hex()}"
#     h_obj.update(hash_input.encode('utf-8'))
#     key = h_obj.digest()

#     decrypted_shares.append(decrypt_tuple(enc_share[0], enc_share[1], enc_share[2], key))

# print(decrypted_shares)



'''
Encryption and Decryption using ssh by sending shares to separate ssh server connections (tested, it works)
'''

# Send each share via separate ssh connection
for share in shares:
    # Parse the share and relevant data
    index, yval = share
    config = remote_configs[index - 1]
    nonce = config.nonce

    # Generate the AES key using the masterkey and the nonce
    h_obj = SHA3_256.new()
    hash_input = f"{DATABASE_MASTERKEY} | {nonce.hex()}"
    h_obj.update(hash_input.encode('utf-8'))
    key = h_obj.digest()

    encrypted_share = encrypt_tuple(share, key, nonce)

    # Encode the data (it threw an error when I tried to serialize bytes objects hahaha)
    encoded_data = [base64.b64encode(item).decode('utf-8') for item in encrypted_share]
    share_json_format = json.dumps(encoded_data)

    print(share_json_format)
    send_remote_file(config, share_json_format)


# Get the shares back from remote server
retrieved_shares = retrieve_remote_files(remote_configs)
print(retrieved_shares)
decrypted_shares = []

# For every retrieved share, we parse it and decrypt it
for retrieved_share in retrieved_shares.values():
    print(retrieved_share)

    # Parse the JSON object
    decoded_data = json.loads(retrieved_share)
    enc_share = tuple(base64.b64decode(item) for item in decoded_data)

    # Generate the database key
    h_obj = SHA3_256.new()
    hash_input = f"{DATABASE_MASTERKEY} | {enc_share[0].hex()}"
    h_obj.update(hash_input.encode('utf-8'))
    key = h_obj.digest()

    # Decrypt
    decrypted_shares.append(decrypt_tuple(enc_share[0], enc_share[1], enc_share[2], key))

print(decrypted_shares)


recovered = reconstruct_secret(decrypted_shares, NUM_HONEST_PARTICIPANTS)

print(recovered)