def extract_text(ocr_results):

    texts = []

    for item in ocr_results:
        text = item.get("text", "").strip()

        if text:
            texts.append(text)

    return texts