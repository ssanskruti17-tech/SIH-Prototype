import os
import json
import streamlit as st

# Fix for CPU oneDNN/PIR issue
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR


@st.cache_resource
def get_ocr_engine():

    return PaddleOCR(
        lang="en",
        enable_mkldnn=False,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )


def run_ocr(image_path):

    ocr_engine = get_ocr_engine()

    results = ocr_engine.predict(image_path)

    detections = []

    for result in results:

        data = result.json

        if callable(data):
            data = data()

        if isinstance(data, str):
            data = json.loads(data)

        if "res" in data:
            data = data["res"]

        texts = data.get("rec_texts", [])
        scores = data.get("rec_scores", [])
        boxes = data.get("rec_boxes", [])

        for i, text in enumerate(texts):

            confidence = 0.0

            if i < len(scores):
                confidence = float(scores[i])

            box = []

            if i < len(boxes):

                if hasattr(boxes[i], "tolist"):
                    box = boxes[i].tolist()
                else:
                    box = boxes[i]

            detections.append({
                "text": str(text),
                "confidence": confidence,
                "box": box
            })

    return detections


def get_average_confidence(results):

    if not results:
        return 0.0

    total = sum(
        item["confidence"]
        for item in results
    )

    return total / len(results)