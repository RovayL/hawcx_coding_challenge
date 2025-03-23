import paramiko
import os

from remote_config_entries import remote_configs
'''
class RemoteConfig:
    def __init__(self, hostname, username, password, remote_path, index, port=22): # Added port, defaults to 22
        self.hostname = hostname
        self.username = username
        self.password = password
        self.remote_path = remote_path
        self.port = port # Store the port number
        self.index = index
'''

def send_remote_file(config, output_string):
    """
    Establishes an SSH connection, creates a text file, and sends it to the remote system.

    Args:
        config (RemoteConfig): The remote configuration struct.
        output_string (str): The string containing the data to write to the file.
    """
    try:
        # Attempt to create the client
        ssh_client = paramiko.SSHClient()
        # Set the key policy
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Be cautious with this in production
        # Connect to the client
        ssh_client.connect(config.hostname, username=config.username, password=config.password, port=config.port) # Added port

        # Store the secret share in a file
        local_filename = f"secret_share.txt"
        with open(local_filename, "w") as f:
            f.write(output_string)

        # Deploy the secure file transfer protocol to transmit the file
        sftp = ssh_client.open_sftp()
        remote_filepath = os.path.join(config.remote_path, local_filename)
        sftp.put(local_filename, remote_filepath)

        # Close the connections
        sftp.close()
        ssh_client.close()
        os.remove(local_filename) #Clean up local file

        print(f"File '{local_filename}' sent to {config.hostname}:{remote_filepath}")

    except Exception as e:
        print(f"Error sending file to {config.hostname}: {e}")

def retrieve_remote_files(configs):
    """
    Establishes SSH connections, retrieves files, and parses triples of integers.

    Args:
        configs (list[RemoteConfig]): A list of remote configuration structs.

    Returns:
        dict: A dictionary where keys are hostnames and values are lists of parsed triples.
    """
    results = {}
    for config in configs:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Be cautious with this in production
            ssh_client.connect(config.hostname, username=config.username, password=config.password, port=config.port) # Added port

            sftp = ssh_client.open_sftp()
            remote_filename = f"secret_share.txt"
            remote_filepath = os.path.join(config.remote_path, remote_filename)

            local_filename = f"retrieved_{config.index}.txt"
            sftp.get(remote_filepath, local_filename)

            sftp.close()
            ssh_client.close()

            with open(local_filename, "r") as f:
                content = f.read().strip()
                triples = []
                if content:
                    try:
                        triple_strings = content.split('\n')
                        for triple_string in triple_strings:
                            int_strings = triple_string.split()
                            if len(int_strings) == 3:
                                triples.append(tuple(map(int, int_strings)))
                            else:
                                print(f"Warning: Invalid triple format in {config.hostname}:{remote_filepath}")
                    except ValueError:
                         print(f"Warning: Invalid integer format in {config.hostname}:{remote_filepath}")
                results[config.hostname] = triples
            os.remove(local_filename) #Clean up local file
            print(f"File '{remote_filename}' retrieved from {config.hostname}")

        except Exception as e:
            print(f"Error retrieving file from {config.hostname}: {e}")
    return results



# Example output string
output_string1 = "1 2 3\n4 5 6\n7 8 9"
output_string2 = "10 11 12\n13 14 15"

# Send files
send_remote_file(remote_configs[0], output_string1)
print("Sent files to user1")
send_remote_file(remote_configs[1], output_string2)
print("Sent files to user2")

# Retrieve and parse files
retrieved_data = retrieve_remote_files(remote_configs)
print("Retrieved data:", retrieved_data)