"""
Utility functions for image upload and validation
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os


def validate_image_file(file):
    """
    Validate image file size and type
    
    Args:
        file: Django UploadedFile object
        
    Raises:
        ValidationError: If file doesn't meet requirements
    """
    # Check file size
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Check file extension
    file_extension = os.path.splitext(file.name)[1].lower().lstrip('.')
    if file_extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"File type '.{file_extension}' is not allowed. Allowed types: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Check MIME type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f"Invalid image type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )
    
    # Verify it's a valid image
    try:
        img = Image.open(file)
        img.verify()
    except Exception as e:
        raise ValidationError(f"Invalid image file: {str(e)}")


def optimize_image(image_file, max_width=1920, max_height=1080, quality=85):
    """
    Optimize image by resizing and compressing
    
    Args:
        image_file: Django UploadedFile object
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
        
    Returns:
        BytesIO object containing optimized image
    """
    img = Image.open(image_file)
    
    # Convert RGBA to RGB if necessary (for JPEG compatibility)
    if img.mode in ('RGBA', 'LA', 'P'):
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = rgb_img
    
    # Resize if necessary
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Save optimized image
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output
