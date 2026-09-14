import re


# =========================================================
# 1. PRODUCT NAME
# =========================================================

def extract_product_name(text):

    patterns = [
        r"(?:Product\s*Name|Commodity\s*Name|Name\s*of\s*Commodity)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:MRP|Net|Manufactured|Packed|Imported|Country|Consumer)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 2. MRP
# =========================================================

def extract_mrp(text):

    patterns = [

        # MRP ₹20
        r"\bM\.?\s*R\.?\s*P\.?\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d+)?)",

        # Maximum Retail Price ₹20
        r"\bMaximum\s+Retail\s+Price\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d+)?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return "₹" + match.group(1)

    return None


# =========================================================
# 3. NET QUANTITY
# =========================================================

def extract_net_quantity(text):

    patterns = [

        # Net Quantity 500 g
        r"(?:Net\s*(?:Quantity|Qty|Content))"
        r"\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(kg|kgs|kilogram|kilograms|g|gm|gram|grams|"
        r"mg|milligram|l|litre|liter|litres|liters|ml)"
        r"\b",

        # NET WT. 500 g
        r"(?:Net\s*(?:Wt|Wt\.|Weight))"
        r"\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(kg|kgs|g|gm|mg|l|ml)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1) + " " + match.group(2)

    return None


# =========================================================
# 4. MANUFACTURER
# =========================================================

def extract_manufacturer(text):

    patterns = [
        r"(?:Manufactured\s+by|Manufactured\s*&|"
        r"Manufacturer|Mfd\.?\s*By)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:Packed|Imported|Country|"
        r"Consumer|MRP|Net)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 5. PACKER
# =========================================================

def extract_packer(text):

    patterns = [
        r"(?:Packed\s+by|Packer|Packaged\s+by|"
        r"Packed\s*&)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:Imported|Country|"
        r"Consumer|MRP|Net|Manufactured)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 6. IMPORTER
# =========================================================

def extract_importer(text):

    patterns = [
        r"(?:Imported\s+by|Importer|"
        r"Imp\.?\s*By)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:Country|Consumer|"
        r"MRP|Net|Manufactured|Packed)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 7. ADDRESS
# =========================================================

def extract_address(text):

    patterns = [
        r"(?:Address|Regd\.?\s*Address|"
        r"Registered\s+Address)"
        r"\s*[:\-]\s*(.+?)(?=\s+(?:Consumer|"
        r"MRP|Net|Manufactured|Packed|Imported|"
        r"Country)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 8. CONSUMER CARE
# =========================================================

def extract_consumer_care(text):

    keywords = [
        "consumer care",
        "consumer complaint",
        "customer care",
        "customer service",
        "customer support",
        "contact us",
        "helpline",
        "toll free",
        "email us"
    ]

    text_lower = text.lower()

    for keyword in keywords:

        if keyword in text_lower:
            return "Detected"

    return None


# =========================================================
# 9. COUNTRY OF ORIGIN
# =========================================================

def extract_country_of_origin(text):

    patterns = [
        r"(?:Country\s+of\s+Origin)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:MRP|Net|Imported|"
        r"Manufactured|Packed|Consumer)|$)",

        r"(?:Made\s+in)"
        r"\s*[:\-]?\s*(.+?)(?=\s+(?:MRP|Net|Imported|"
        r"Manufactured|Packed|Consumer)|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================================================
# 10. DATES
# =========================================================

def extract_dates(text):

    dates = {}

    # Manufacturing / MFD date
    manufacturing_patterns = [
        r"(?:MFG|MFD|Manufactured\s+on|"
        r"Manufacturing\s+Date|Date\s+of\s+Manufacture)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",

        r"(?:MFG|MFD|Manufactured)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{4})"
    ]

    for pattern in manufacturing_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            dates["manufacturing_date"] = match.group(1)
            break

    # Packing date
    packing_patterns = [
        r"(?:Packed\s+on|Packing\s+Date|"
        r"Date\s+of\s+Packing)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",

        r"(?:Packed\s+on|Packing\s+Date)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{4})"
    ]

    for pattern in packing_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            dates["packing_date"] = match.group(1)
            break

    # Import date
    import_patterns = [
        r"(?:Date\s+of\s+Import|Imported\s+on|"
        r"Import\s+Date)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    ]

    for pattern in import_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            dates["import_date"] = match.group(1)
            break

    # Best before
    best_before_patterns = [
        r"(?:Best\s+Before)"
        r"\s*[:\-]?\s*(.{1,40}?)(?=\s+(?:MRP|Net|"
        r"Consumer|Manufactured|Packed)|$)",

        r"(?:Use\s+By|Expiry|Expires)"
        r"\s*[:\-]?\s*(.{1,30}?)(?=\s+(?:MRP|Net|"
        r"Consumer|Manufactured|Packed)|$)"
    ]

    for pattern in best_before_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            dates["best_before"] = match.group(1).strip()
            break

    return dates


# =========================================================
# 11. OTHER DECLARATIONS
# =========================================================

def extract_declarations(text):

    declarations = []

    keywords = [
        "maximum retail price",
        "net quantity",
        "net qty",
        "manufacturer",
        "manufactured by",
        "packer",
        "packed by",
        "importer",
        "imported by",
        "country of origin",
        "consumer care",
        "customer care",
        "best before",
        "use by",
        "expiry",
        "unit sale price"
    ]

    text_lower = text.lower()

    for keyword in keywords:

        if keyword in text_lower:
            declarations.append(keyword)

    return declarations


# =========================================================
# 12. MAIN PARSER
# =========================================================

def parse_product(ocr_results):

    # Get text from OCR results
    texts = []

    for item in ocr_results:

        text = item.get("text", "").strip()

        if text:
            texts.append(text)

    # Combine OCR text
    combined_text = " ".join(texts)

    # Extract all product information
    product = {

        "product_name": extract_product_name(
            combined_text
        ),

        "mrp": extract_mrp(
            combined_text
        ),

        "net_quantity": extract_net_quantity(
            combined_text
        ),

        "manufacturer": extract_manufacturer(
            combined_text
        ),

        "packer": extract_packer(
            combined_text
        ),

        "importer": extract_importer(
            combined_text
        ),

        "address": extract_address(
            combined_text
        ),

        "consumer_care": extract_consumer_care(
            combined_text
        ),

        "country_of_origin": extract_country_of_origin(
            combined_text
        ),

        "dates": extract_dates(
            combined_text
        ),

        "declarations": extract_declarations(
            combined_text
        ),

        "raw_text": combined_text
    }

    return product