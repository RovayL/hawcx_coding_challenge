# Welcome to a deployment of remote Shamir Secret Sharing

The entry point of the program is `main.py`, with the other files acting as supporting libraries to assist the cryptography and distributed systems.

**NOTE:** `main.py` can execute both on-system shamir secret sharing and distributed system secret sharing. The on system code is commented out but placed at the start of the program. The distributed system is placed at the bottom of the program. To run a particular system, simply comment or uncomment out the relevant code. Both schemes create a final object called `decrypted_shares`, and therefore `recovered = reconstruct_secret(decrypted_shares, NUM_HONEST_PARTICIPANTS)` is the final phase of both programs that uses Lagrange interpolation of the shamir secret sharing scheme to reconstruct the secret.

To run the code, simply run `python3 main.py` in the terminal. If the compiler complains about a missing dependency, simply run `pip install <DEPENDENCY>` or another similar command. Dependencies are used to manage cryptography primitives and distributed system primitives. In particular:

-> `paramiko`: Dependency is used for ssh connections and secure file transfer protocol for the distributed system
-> `pycryptodome`: Dependency is used for AES-GCM encryption and authentication, as well as SHA-3 hashing

Each file will now be described below:

## `main.py`
The entrypoint of the secret sharing scheme. Run `python3 main.py`, after choosing which scheme to use via commenting/uncommenting out the relevant code. The constants `DATABASE_MASTERKEY`, `NUM_HONEST_PARTICIPANTS`, `NUM_PARTICIPANTS`, `SHAMIR_SECRET`, and `SHAMIR_SEED` do exactly what they sound like they should do, with `SHAMIR_SEED` being used to seed the random polynomial construction used in `shamir_secret_sharing.py`. `main.py` has aready been described above.

## `shamir_secret_sharing.py`
Peforms the shamir secret sharing algorithm. `split_secret` generates secret shares given a secret and random seed for the polynomial. `reconstruct_secret` takes the shares and reconsructs the secret using Lagrange Interpolation. `MODULUS` is a constant defining the group modulus so as to allow for field element arithmetic. **NOTE:** The constants `NUM_HONEST_PARTICIPANTS` and `NUM_PARTICIPANTS` is overrided in `main.py`, these constants are only in place if no other constants are provided.

## `romu_quad_implementation.py`
[Source paper](https://arxiv.org/pdf/2002.11331)
Performs nonlinear-shift register operations, and is a simple implementation based on the paper. Should be more secure than a typical linear feedback shift register due to the introduction of non-linear operations (e.g. multiplication and bit rotations), and it should be more performant, in that if it is implemented in `C`, it should have very low register pressure and require few cycles per compute.

Is used in `shamir_secret_sharing.py` for the random polynomial construction

## `aes.py`
Is a wrapper for AES-GCM to encrypt, decrypt, and authenticate secret shares as they are sent remotely. Nonces are used to increase enthropy and therefore security. `JSON` objects are used so as to wrap potentially very large integers, as the original implementation with `structs` failed due to the integers in the shares overflowing their capacity.

## `remote_transmit.py`
Creates `ssh` connections and uses `sftp` to send encrypted secret shares to database configurations. The configurations contain the following information:

```
class RemoteConfig:
    def __init__(self, hostname, username, password, remote_path, index, port=22, nonce=0):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.remote_path = remote_path
        self.port = port
        self.nonce = nonce
        self.index = index
```

The function `send_remote_file` takes in a `RemoteConfig` object and a string, and stores the string in a file called `secret_share.txt` in the directory `remote_path` for the specified `hostname` and `username`. The attribute `port` was added because my server system multiplexes via ports, so it is necessary to distinguish between ports in order for my system to operate.

The function `retrieve_remote_files` takes in a list of `RemoteConfig` objects and retrieves all the relevant data (that is stored in `secret_share.txt`) and stores it in a dictionary, indexed via the `index` attribute.

## `dummy_remote_config_entries.py`
Not the real config file (on my system, the real config file is called **`remote_config_entries.py`**), however the actual config file is exactly the same except for each `remote_configs.append(RemoteConfig("host_or_IP_0", "user_0", "password_0", "/file/location_0", index_0, port_0))`, legitimate values are placed.
