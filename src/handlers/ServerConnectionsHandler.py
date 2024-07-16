import configparser, paramiko
from pathlib import Path
from handlers.DatabaseHandler import get_current_dir

def establish_ssh_connection():
    # Get the SSH credentials from the config file
    config_file = Path(get_current_dir(subdirectory="../credentials/conf.ini"))
    assert config_file.exists(), "conf.ini file not found"

    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            config["nat-server"]["server"],
            username=config["nat-server"]["username"],
            password=config["nat-server"]["password"]
        )
        return ssh
    except Exception as e:
        print(f"Failed to establish SSH connection: {str(e)}")
        return None

