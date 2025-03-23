from shamir_secret_sharing import split_secret, reconstruct_secret

shares = split_secret(20, 2304920340)

print(shares)

recovered = reconstruct_secret(shares)

print(recovered)