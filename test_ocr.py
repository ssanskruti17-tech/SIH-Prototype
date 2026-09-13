from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)

image_path = "test.jpg"

results = ocr.predict(image_path)

for result in results:
    print(result.json)