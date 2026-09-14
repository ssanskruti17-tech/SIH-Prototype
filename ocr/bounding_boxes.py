def get_bounding_boxes(ocr_results):

    boxes = []

    for item in ocr_results:

        box = item.get("box", [])

        boxes.append({
            "text": item.get("text", ""),
            "box": box
        })

    return boxes