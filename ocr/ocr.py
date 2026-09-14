from ocr.run_ocr import run_ocr
from ocr.extract_text import extract_text
from ocr.bounding_boxes import get_bounding_boxes
from ocr.confidence import get_ocr_confidence
from ocr.combine_text import combine_text


def process_ocr(image_path):

    # Step 1: Run PaddleOCR
    ocr_results = run_ocr(image_path)

    # Step 2: Extract text
    texts = extract_text(ocr_results)

    # Step 3: Get bounding boxes
    boxes = get_bounding_boxes(ocr_results)

    # Step 4: Calculate confidence
    confidence = get_ocr_confidence(ocr_results)

    # Step 5: Combine text
    combined_text = combine_text(texts)

    return {
        "raw_results": ocr_results,
        "texts": texts,
        "boxes": boxes,
        "confidence": confidence,
        "combined_text": combined_text
    }