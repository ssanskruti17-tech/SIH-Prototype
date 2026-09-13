import os
from datetime import datetime

from scan.opencv_utils import (
    load_image,
    check_image_validity,
    check_resolution,
    analyze_image_quality
)

from scan.pillow_utils import (
    open_image,
    get_image_format,
    get_image_metadata,
    save_image
)


UPLOAD_DIR = "uploads"


def scan_product(front_image, back_image=None):
    """
    Main scanning function.

    It connects OpenCV and Pillow to:
    1. Validate images
    2. Analyze image quality
    3. Save images
    4. Collect metadata
    """

    result = {
        "status": "FAILED",
        "front_image": None,
        "back_image": None,
        "metadata": {},
        "errors": []
    }

    # =====================================================
    # FRONT IMAGE
    # =====================================================

    if front_image is None:

        result["errors"].append(
            "Front image is required."
        )

        return result

    try:

        # Get bytes from Streamlit UploadedFile
        if hasattr(front_image, "getvalue"):
          front_bytes = front_image.getvalue()
        else:
         front_image.seek(0)
        front_bytes = front_image.read()
        front_image.seek(0)

        # -------------------------------------------------
        # OpenCV
        # -------------------------------------------------

        cv_image = load_image(front_bytes)

        if not check_image_validity(cv_image):

            result["errors"].append(
                "Front image is invalid."
            )

            return result

        resolution_ok, resolution_message = (
            check_resolution(cv_image)
        )

        if not resolution_ok:

            result["errors"].append(
                f"Front image: {resolution_message}"
            )

            return result

        quality = analyze_image_quality(
            cv_image
        )

        if quality["quality"] != "Good":

            result["errors"].append(
                f"Front image quality: "
                f"{quality['quality']}"
            )

            return result

        # -------------------------------------------------
        # Pillow
        # -------------------------------------------------

        pil_image = open_image(front_bytes)

        if pil_image is None:

            result["errors"].append(
                "Pillow could not open front image."
            )

            return result

        image_format = get_image_format(
            pil_image
        )

        # -------------------------------------------------
        # Save image
        # -------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        front_filename = (
            f"{timestamp}_front.jpg"
        )

        front_path = os.path.join(
            UPLOAD_DIR,
            front_filename
        )

        saved = save_image(
            pil_image,
            front_path
        )

        if not saved:

            result["errors"].append(
                "Could not save front image."
            )

            return result

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        metadata = get_image_metadata(
            pil_image,
            front_bytes
        )

        metadata["original_format"] = image_format

        metadata["quality"] = quality

        result["front_image"] = front_path

        result["metadata"]["front"] = metadata


    except Exception as e:

        result["errors"].append(
            f"Front image error: {str(e)}"
        )

        return result


    # =====================================================
    # BACK IMAGE
    # =====================================================

    if back_image is not None:

        try:

            if hasattr(back_image, "getvalue"):
             back_bytes = back_image.getvalue()
            else:
             back_image.seek(0)
             back_bytes = back_image.read()
             back_image.seek(0)

            # -------------------------------------------------
            # OpenCV
            # -------------------------------------------------

            cv_image = load_image(
                back_bytes
            )

            if not check_image_validity(
                cv_image
            ):

                result["errors"].append(
                    "Back image is invalid."
                )

                return result

            resolution_ok, resolution_message = (
                check_resolution(cv_image)
            )

            if not resolution_ok:

                result["errors"].append(
                    f"Back image: {resolution_message}"
                )

                return result

            quality = analyze_image_quality(
                cv_image
            )

            if quality["quality"] != "Good":

                result["errors"].append(
                    f"Back image quality: "
                    f"{quality['quality']}"
                )

                return result

            # -------------------------------------------------
            # Pillow
            # -------------------------------------------------

            pil_image = open_image(
                back_bytes
            )

            if pil_image is None:

                result["errors"].append(
                    "Pillow could not open back image."
                )

                return result

            image_format = get_image_format(
                pil_image
            )

            # -------------------------------------------------
            # Save
            # -------------------------------------------------

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S_%f"
            )

            back_filename = (
                f"{timestamp}_back.jpg"
            )

            back_path = os.path.join(
                UPLOAD_DIR,
                back_filename
            )

            saved = save_image(
                pil_image,
                back_path
            )

            if not saved:

                result["errors"].append(
                    "Could not save back image."
                )

                return result

            # -------------------------------------------------
            # Metadata
            # -------------------------------------------------

            metadata = get_image_metadata(
                pil_image,
                back_bytes
            )

            metadata["original_format"] = image_format

            metadata["quality"] = quality

            result["back_image"] = back_path

            result["metadata"]["back"] = metadata


        except Exception as e:

            result["errors"].append(
                f"Back image error: {str(e)}"
            )

            return result


    # =====================================================
    # SUCCESS
    # =====================================================

    result["status"] = "SUCCESS"

    return result