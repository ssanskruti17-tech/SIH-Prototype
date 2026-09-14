from ocr.ocr import process_ocr


image_path = "front.jpeg"

result = process_ocr(image_path)


print("\n========== OCR TEST ==========")

print("\nDetected Text:")
for text in result["texts"]:
    print("-", text)

print("\nOCR Confidence:")
print(result["confidence"])

print("\nBounding Boxes:")

for item in result["boxes"]:
    print(item)

print("\nCombined Text:")
print(result["combined_text"])

print("\n==============================")