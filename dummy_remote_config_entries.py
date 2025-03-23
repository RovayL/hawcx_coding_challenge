class RemoteConfig:
    def __init__(self, hostname, username, password, remote_path, index, port=22, nonce=0): # Added port, defaults to 22
        self.hostname = hostname
        self.username = username
        self.password = password
        self.remote_path = remote_path
        self.port = port
        self.nonce = nonce
        self.index = index

# # Global list of structs
remote_configs = []


# Example usage:
# Create example remote configs
remote_configs.append(RemoteConfig("host_or_IP_0", "user_0", "password_0", "/file/location_0", index_0, port_0))
# Nonce data can be added here, but it is probably best to do it during the key generation phase