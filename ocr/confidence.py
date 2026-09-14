def get_ocr_confidence(ocr_results):

    if not ocr_results:
        return 0.0

    total_confidence = 0.0

    for item in ocr_results:
        total_confidence += float(
            item.get("confidence", 0.0)
        )

    average_confidence = (
        total_confidence / len(ocr_results)
    )

    return round(average_confidence, 2)