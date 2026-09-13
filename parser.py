import re


def extract_mrp(text):

    pattern = r"(?:MRP|M\.R\.P)\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d+)?)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return "₹" + match.group(1)

    return None


def extract_quantity(text):

    pattern = (
        r"(?:Net\s*Quantity|Net\s*Qty|"
        r"Net\s*Content|Quantity)"
        r"\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(kg|g|gm|mg|l|ml)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return (
            match.group(1)
            + " "
            + match.group(2)
        )

    return None


def extract_manufacturer(text):

    pattern = (
        r"(?:Manufactured\s*by|"
        r"Manufactured\s*&|"
        r"Manufacturer)"
        r"\s*[:\-]?\s*(.+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


def extract_importer(text):

    pattern = (
        r"(?:Imported\s*by|"
        r"Importer)"
        r"\s*[:\-]?\s*(.+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


def extract_consumer_care(text):

    keywords = [
        "consumer care",
        "customer care",
        "customer service",
        "contact us",
        "helpline",
        "toll free"
    ]

    text_lower = text.lower()

    for keyword in keywords:

        if keyword in text_lower:
            return "Detected"

    return None


def parse_product(ocr_results):

    combined_text = " ".join(
        item["text"]
        for item in ocr_results
    )

    return {

        "mrp": extract_mrp(combined_text),

        "quantity": extract_quantity(combined_text),

        "manufacturer": extract_manufacturer(
            combined_text
        ),

        "importer": extract_importer(
            combined_text
        ),

        "consumer_care": extract_consumer_care(
            combined_text
        )
    }