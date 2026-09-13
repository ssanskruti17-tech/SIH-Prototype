from ocr import run_ocr, extract_text, get_confidence


image_path = "test.jpg"

results = run_ocr(image_path)

print("\n========== DETECTED TEXT ==========\n")

for item in results:

    print(
        f"{item['text']} "
        f"(confidence: {item['confidence']:.2f})"
    )


print("\n========== COMBINED TEXT ==========\n")

print(extract_text(results))


print("\n========== AVERAGE CONFIDENCE ==========\n")

print(get_confidence(results))