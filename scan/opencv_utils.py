import cv2
import numpy as np


def load_image(image_bytes):
    """
    Load image using OpenCV.
    """

    if not image_bytes:
        return None

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    return image


def check_image_validity(image):
    """
    Check whether OpenCV successfully loaded the image.
    """

    if image is None:
        return False

    return True


def check_resolution(image, min_width=300, min_height=300):
    """
    Check image resolution.
    """

    if image is None:
        return False, "Image could not be loaded."

    height, width = image.shape[:2]

    if width < min_width or height < min_height:
        return False, (
            f"Resolution too low: {width}x{height}. "
            f"Minimum required is {min_width}x{min_height}."
        )

    return True, f"Resolution is good: {width}x{height}."


def analyze_image_quality(image):
    """
    Perform basic image quality analysis using OpenCV.

    Checks:
    - Brightness
    - Sharpness / blur
    """

    if image is None:
        return {
            "brightness": 0,
            "sharpness": 0,
            "quality": "Invalid"
        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    brightness = float(np.mean(gray))

    sharpness = float(
        cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()
    )

    if brightness < 30:
        quality = "Too Dark"

    elif brightness > 245:
        quality = "Too Bright"

    elif sharpness < 20:
        quality = "Blurry"

    else:
        quality = "Good"

    return {
        "brightness": round(brightness, 2),
        "sharpness": round(sharpness, 2),
        "quality": quality
    }