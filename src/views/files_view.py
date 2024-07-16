from flask import Blueprint, jsonify, request, send_file, Response
from handlers.StorageHandler import get_file_system_structure, get_storage_info, remove_file_or_folder, handle_download
from handlers.ServerConnectionsHandler import establish_ssh_connection
from werkzeug.utils import secure_filename
import os, io, zipfile


# Create a Blueprint for files view
files_view = Blueprint('files_view', __name__)

@files_view.route('/storage-usage', methods=["GET"])
def storage_usage():
    
    storage_info = get_storage_info()
    
    return jsonify(storage_info)

@files_view.route('/file-system-structure/<id>', methods=["GET"])
@files_view.route('/file-system-structure/<id>/<path:click_object>', methods=["GET"])
def file_system_structure(id, click_object=None):
    file_system_structure = get_file_system_structure(id, click_object)
    return jsonify(file_system_structure)

@files_view.route('/upload', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # Save the uploaded file to the server
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    return 'File uploaded successfully'

@files_view.route('/create-folder', methods=["POST"])
def create_folder():
    folder_name = request.form.get('folder_name')
    path = request.form.get('path')

    try:
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], path, folder_name))
        return 'Folder created successfully'
    except FileExistsError:
        return 'Folder already exists'
    
# Route to handle file removal (for DELETE requests)
@files_view.route('/remove/<user_id>/<path:file_or_folder_name>', methods=['DELETE'])
def remove(user_id, file_or_folder_name):
    success, message = remove_file_or_folder(user_id, file_or_folder_name)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 500
    
# Route to handle the download of a file (for GET requests)
@files_view.route('/download/<user_id>/<path:file_or_folder_name>', methods=['GET'])
def download(user_id, file_or_folder_name):
    content, error = handle_download(user_id, file_or_folder_name)
    
    if error:
        return jsonify({"error": error}), 500
    
    if isinstance(content, bytes):
        # If content is a single file, send it as an attachment
        return send_file(io.BytesIO(content), download_name=file_or_folder_name, as_attachment=True)
    elif isinstance(content, dict):
        # If content is a folder, create a zip archive and send it as an attachment
        zip_bytes = io.BytesIO()
        with zipfile.ZipFile(zip_bytes, 'w') as zf:
            for file_name, file_content in content.items():
                zf.writestr(file_name, file_content)
        zip_bytes.seek(0)
        return send_file(zip_bytes, download_name=f"{file_or_folder_name}.zip", as_attachment=True)
    else:
        return jsonify({"error": "Unknown content type"}), 500