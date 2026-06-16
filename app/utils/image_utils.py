import os
from datetime import datetime
import uuid


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']
MAX_FILE_SIZE = 5 * 1024 * 1024  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_post_image(file, upload_folder=None):
    
    # Valida que exista el archivo
    if not file or file.filename == '':
        return None, "No se seleccionó archivo"
    
    # Valida extensión
    if not allowed_file(file.filename):
        return None, "Formato de archivo no permitido. Use: PNG, JPG, JPEG, GIF, WebP"
    
    # Valida tamaño
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > MAX_FILE_SIZE:
        return None, "El archivo es demasiado grande. Máximo 5MB"
    file.seek(0)

    # Define carpeta de uploads
    if not upload_folder:
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    
    # Genera nombre único
    ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    filename = f"post_{timestamp}_{unique_id}.{ext}"
    
    # Guarda archivo en static/images
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    return filename, None
