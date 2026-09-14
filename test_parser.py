from parser.parser import parse_product


# -----------------------------------------
# Sample OCR result
# -----------------------------------------

ocr_results = [
    {
        "text": "ABC Premium Biscuits",
        "confidence": 0.96
    },
    {
        "text": "MRP ₹50",
        "confidence": 0.95
    },
    {
        "text": "Net Quantity 200 g",
        "confidence": 0.94
    },
    {
        "text": "Manufactured by ABC Foods Pvt Ltd",
        "confidence": 0.93
    },
    {
        "text": "Packed by XYZ Packers",
        "confidence": 0.92
    },
    {
        "text": "Imported by ABC India",
        "confidence": 0.91
    },
    {
        "text": "Address: Mumbai, Maharashtra",
        "confidence": 0.90
    },
    {
        "text": "Consumer Care: 1800-123-456",
        "confidence": 0.89
    },
    {
        "text": "Country of Origin: Japan",
        "confidence": 0.94
    },
    {
        "text": "MFD: 08/2026",
        "confidence": 0.93
    },
    {
        "text": "Best Before: 12 Months",
        "confidence": 0.92
    }
]


# -----------------------------------------
# Run parser
# -----------------------------------------

result = parse_product(ocr_results)


# -----------------------------------------
# Display result
# -----------------------------------------

print("\n========== PARSER TEST ==========")

print("\nProduct Name:")
print(result["product_name"])

print("\nMRP:")
print(result["mrp"])

print("\nNet Quantity:")
print(result["net_quantity"])

print("\nManufacturer:")
print(result["manufacturer"])

print("\nPacker:")
print(result["packer"])

print("\nImporter:")
print(result["importer"])

print("\nAddress:")
print(result["address"])

print("\nConsumer Care:")
print(result["consumer_care"])

print("\nCountry of Origin:")
print(result["country_of_origin"])

print("\nDates:")
print(result["dates"])

print("\nDeclarations Detected:")
for declaration in result["declarations"]:
    print("-", declaration)

print("\nRaw Text:")
print(result["raw_text"])

print("\n=================================")
print("PARSER TEST COMPLETED")
print("=================================")