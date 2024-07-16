import configparser, os, zipfile, io
from pathlib import Path
from flask import jsonify, send_file
from handlers.DatabaseHandler import get_current_dir
from handlers.ServerConnectionsHandler import establish_ssh_connection


def get_storage_info():
    # Example data, replace with actual storage calculation logic
    total_storage = 120  # GB
    used_storage = 50    # GB
    percentage_used = (used_storage / total_storage) * 100
    
    ssh = establish_ssh_connection()
    
    # Execute the command to get the storage usage in the SSD disk (in the /mnt/ssd/ directory)
    _, stdout, _ = ssh.exec_command("df -h /mnt/ssd/")
    
    # Get the output of the command
    output = stdout.readlines()
    
    # Close the SSH connection
    ssh.close()
    
    # Parse the output to get the storage usage
    for line in output:
        if "/mnt/ssd" in line:
            data = line.split()
            storage_usage = data[4]
            capacity = data[1]
            used_storage = data[2]
            file_system = data[0]
            mounted_location = data[5]
            percentage_used = int(storage_usage[:-1])
            break
    
    return {
                "percentage_used": percentage_used, \
                "capacity": capacity + 'B' if capacity[-1].isupper() else capacity, \
                "used_storage": used_storage + 'B' if used_storage[-1].isupper() else used_storage, \
                "file_system": file_system, \
                "mounted_location": mounted_location
            }

def get_file_system_structure(user_id, click_object):
    # Get the SSH credentials from the config file
    config_file = Path(get_current_dir(subdirectory="../credentials/conf.ini"))
    assert config_file.exists(), "conf.ini file not found"

    config = configparser.ConfigParser()
    config.read(config_file)
    
    ssh = establish_ssh_connection()
    
    # Construct the command to get the file system structure
    directory = f"/mnt/ssd/{user_id}/{click_object}" if click_object else f"/mnt/ssd/{user_id}"
    command = f"ls -l {directory}"
    
    # Execute the command
    _, stdout, _ = ssh.exec_command(command)
    
    # Get the output of the command
    output = stdout.readlines()
    
    # Close the SSH connection
    ssh.close()
    
    # Parse the output to get the file system structure
    file_system_structure = []
    for line in output:
        data = line.split()
        if len(data) >= 9:
            file_system_structure.append({
                "permissions": data[0],
                "links": data[1],
                "owner": data[2],
                "group": data[3],
                "size": data[4],
                "date": " ".join(data[5:7]),
                "time": data[7],
                "name": "".join(data[8:])
            })

    # Order to show directories first and then files
    file_system_structure.sort(key=lambda x: x['permissions'][0] != 'd')

    return file_system_structure


def remove_file_or_folder(user_id, file_or_folder_name):
    ssh = establish_ssh_connection()
    
    if not ssh:
        return False, "Failed to establish SSH connection"
    
    try:
        # Construct the path to the file or folder
        path = f"/mnt/ssd/{user_id}/{file_or_folder_name}"
        
        # Execute the rm command
        command = f"rm -rf {path}"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Check if there were any errors
        error = stderr.read().decode().strip()
        if error:
            return False, f"Failed to remove {file_or_folder_name}: {error}"
        
        return True, f"{file_or_folder_name} removed successfully"
    
    except Exception as e:
        return False, f"Error removing {file_or_folder_name}: {str(e)}"
    
    finally:
        ssh.close()

# Function to retrieve file or folder content from SSH server
def get_file_or_folder_content(ssh, user_id, file_or_folder_name):
    try:
        remote_path = f'/path/to/files/{user_id}/{file_or_folder_name}'
        
        # Check if the path is a file or a folder
        _, stdout, stderr = ssh.exec_command(f'[ -f "{remote_path}" ] && echo "file" || echo "folder"')
        file_type = stdout.read().strip().decode('utf-8')
        
        if file_type == 'file':
            # Retrieve file content
            stdin, stdout, stderr = ssh.exec_command(f'cat "{remote_path}"')
            file_content = stdout.read()
            return file_content, True  # True indicates file
        elif file_type == 'folder':
            # Create zip archive of folder contents
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                add_folder_contents_to_zip(ssh, zip_file, remote_path)
            
            zip_buffer.seek(0)
            return zip_buffer.read(), False  # False indicates folder (zip archive)
        else:
            return None, None  # Error: neither file nor folder
    except Exception as e:
        print(f"Error retrieving file or folder content: {e}")
        return None, None

# Helper function to add folder contents recursively to a zip archive
def add_folder_contents_to_zip(ssh, zip_file, folder_path):
    # Get list of files and directories in the folder
    stdin, stdout, stderr = ssh.exec_command(f'cd "{folder_path}" && ls -A1')
    contents = stdout.read().splitlines()
    
    for item in contents:
        item = item.decode('utf-8')
        item_path = os.path.join(folder_path, item)
        
        # Check if the item is a file or a directory
        _, stdout, stderr = ssh.exec_command(f'[ -f "{item_path}" ] && echo "file" || echo "folder"')
        file_type = stdout.read().strip().decode('utf-8')
        
        if file_type == 'file':
            # Add file to zip archive
            zip_file.write(item_path, arcname=os.path.basename(item_path))
        elif file_type == 'folder':
            # Recursively add contents of subfolder to zip archive
            add_folder_contents_to_zip(ssh, zip_file, item_path)

# Function to handle downloading file or folder content
def handle_download(user_id, file_or_folder_name):
    # Establish an SSH connection
    ssh = establish_ssh_connection()
    if not ssh:
        return None, {"error": "Failed to establish SSH connection"}
    
    # Get file or folder content from SSH server
    content, is_file = get_file_or_folder_content(ssh, user_id, file_or_folder_name)
    if content is None:
        ssh.close()
        return None, {"error": "Failed to retrieve file or folder content"}
    
    ssh.close()
    return content, None