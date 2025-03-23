from romu_quad_implementation import RomuQuad

MODULUS = 2**127 - 1
NUM_HONEST_PARTICIPANTS = 3  # Example threshold (k)
NUM_PARTICIPANTS = 5         # Example number of shares (n)

def split_secret(secret, seed):
    """
    Splits a secet into many shares, stored as a set of tuples, with indecies related for later reconstruction

    Args:
        secret (int): The secret that is a field element to be split
        seed (int): The string containing the data to write to the file.

    Returns:
        shares (list): A list of tuples of (x,y) pairs comprising of a secret share
    """
    if secret >= MODULUS:
        raise ValueError("Secret must be less than the modulus.")
    t = NUM_HONEST_PARTICIPANTS
    rng = RomuQuad(seed)
    coefficients = [secret]
    # Coefficients for polynomial are randomly generated using a pseudorandom number generator
    for _ in range(t - 1):
        coeff = rng.random() % MODULUS
        coefficients.append(coeff)

    # Shares are created via evaluating polynomial at various points
    shares = []
    for x in range(1, NUM_PARTICIPANTS + 1):
        y = 0
        for i in range(t):
            y = (y + coefficients[i] * (x ** i)) % MODULUS
        shares.append((x, y))
    return shares

def reconstruct_secret(shares):
    """
    Recieves at least NUM_HONEST_PARTICIPANTS shares, stored as a set of tuples, and returns the original secret

    Args:
        shares (list): A list of tuples of (x,y) pairs comprising of a secret share

    Returns:
        secret (int): The original secret that was inputted at the start of the scheme
    """
    if len(shares) < NUM_HONEST_PARTICIPANTS:
        raise ValueError("Not enough shares to reconstruct the secret.")

    # Typical Lagrange interpolation, not much more to say
    p = MODULUS
    secret = 0
    for i in range(len(shares)):
        xi, yi = shares[i]
        numerator = 1
        denominator = 1
        for j in range(len(shares)):
            if j == i:
                continue
            xj = shares[j][0]
            numerator = (numerator * (-xj)) % p
            denominator = (denominator * (xi - xj)) % p
        inv_denominator = pow(denominator, -1, p)
        li = (numerator * inv_denominator) % p
        secret = (secret + yi * li) % p
    return secret