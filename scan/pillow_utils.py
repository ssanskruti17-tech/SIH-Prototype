import os
from PIL import Image


def open_image(image_bytes):
    """
    Open image using Pillow.
    """

    if not image_bytes:
        return None

    try:
        image = Image.open(
            __import__("io").BytesIO(image_bytes)
        )

        return image

    except Exception:
        return None


def get_image_format(image):
    """
    Get image format using Pillow.
    """

    if image is None:
        return None

    return image.format


def get_image_metadata(image, image_bytes):
    """
    Get image metadata using Pillow.
    """

    if image is None:
        return {}

    metadata = {
        "format": image.format,
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "file_size_kb": round(
            len(image_bytes) / 1024,
            2
        )
    }

    # Check EXIF metadata
    exif_data = image.getexif()

    metadata["exif_available"] = bool(exif_data)

    return metadata


def save_image(image, save_path):
    """
    Save image using Pillow.
    """

    if image is None:
        return False

    try:

        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        # Convert to RGB so JPEG saving works
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(
            save_path,
            format="JPEG",
            quality=95
        )

        return True

    except Exception:
        return False