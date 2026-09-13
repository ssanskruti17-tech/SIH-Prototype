def validate_product(product, ocr_results):

    issues = []

    if not product["mrp"]:
        issues.append(
            "MRP was not detected."
        )

    if not product["quantity"]:
        issues.append(
            "Net quantity was not detected."
        )

    if not product["manufacturer"]:
        issues.append(
            "Manufacturer details were not detected."
        )

    if not product["importer"]:
        issues.append(
            "Importer details were not detected."
        )

    if not product["consumer_care"]:
        issues.append(
            "Consumer care details were not detected."
        )

    if ocr_results:

        average_confidence = (
            sum(
                item["confidence"]
                for item in ocr_results
            )
            / len(ocr_results)
        )

        if average_confidence < 0.70:

            issues.append(
                "OCR confidence is low. "
                "Manual review recommended."
            )

    else:

        issues.append(
            "No text detected from the image."
        )

    if not issues:

        status = "COMPLIANT"

    else:

        status = "NEEDS REVIEW"

    return {
        "status": status,
        "issues": issues
    }