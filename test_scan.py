from scan.scan import scan_product


# Test image
front_image_path = "front.jpeg"


# Open image like a file upload
with open(front_image_path, "rb") as front_file:

    result = scan_product(front_file)


print("\n========== SCAN TEST ==========")

print("Status:", result["status"])

print("\nFront Image:")
print(result["front_image"])

print("\nBack Image:")
print(result["back_image"])

print("\nMetadata:")
print(result["metadata"])

print("\nErrors:")
print(result["errors"])

print("\n================================")