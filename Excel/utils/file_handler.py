ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'webp'},
    'document': {'xlsx', 'xls', 'csv'}  
}

def is_file_valid(uploaded_file, file_type):
    file_extension = uploaded_file.name.rsplit('.', 1)[-1].lower()
    allowed_extensions = ALLOWED_EXTENSIONS.get(file_type)
    return bool(allowed_extensions and file_extension in allowed_extensions)
