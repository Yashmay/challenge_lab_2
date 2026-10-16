
from collections import Counter
from pathlib import Path
from PIL import Image
import math

# Input and output files
INPUT_FILE = Path("aes.bmp")
OUTPUT_FILE = Path("ecb_visualization.png")

AES_BLOCK_SIZE = 16
BMP_HEADER_SIZE = 54

# Read the encrypted file
data = INPUT_FILE.read_bytes()

print("=== File Information ===")
print(f"File size: {len(data)} bytes")
print(f"First 54 bytes: {data[:54].hex(' ').upper()}")
print(f"BMP signature: {data[:2]!r}")
print(f"Valid BM signature: {data[:2] == b'BM'}")

# 1. Analyse repeated AES blocks
print("\n=== ECB Block Analysis ===")

complete_length = len(data) // AES_BLOCK_SIZE * AES_BLOCK_SIZE
blocks = [
    data[i:i + AES_BLOCK_SIZE]
    for i in range(0, complete_length, AES_BLOCK_SIZE)
]

counts = Counter(blocks)
unique_blocks = len(counts)
repeated_blocks = sum(
    count - 1 for count in counts.values() if count > 1
)

print(f"Complete 16-byte blocks: {len(blocks)}")
print(f"Unique blocks: {unique_blocks}")
print(f"Repeated block occurrences: {repeated_blocks}")
print(f"Unique block percentage: "
      f"{unique_blocks / len(blocks) * 100:.2f}%"
      if blocks else "No complete blocks")

print("\nMost common blocks:")
for block, count in counts.most_common(10):
    print(f"{block.hex().upper()} : {count} occurrence(s)")

# 2. Inspect whether the file length suggests
# an encrypted pixel region after a 54-byte header
print("\n=== Bitmap Size Investigation ===")

pixel_data = data[54:]

print(f"Bytes after offset 54: {len(pixel_data)}")
print(f"Divisible by 16: {len(pixel_data) % 16 == 0}")

# 3. Reconstruct a visualization.
# This assumes 640x480 pixels, 24 bits per pixel,
# with 3 bytes per pixel and no row padding.
width = 640
height = 480
expected_size = width * height * 3

if len(pixel_data) == expected_size:
    image = Image.frombytes("RGB", (width, height), pixel_data)
    image.save(OUTPUT_FILE)
    print(f"\nVisualization saved to: {OUTPUT_FILE.resolve()}")
else:
    print(f"\nExpected pixel bytes: {expected_size}")
    print(f"Actual pixel bytes: {len(pixel_data)}")
    print("The assumed dimensions do not match.")
    print("Try alternative offsets or image dimensions.")
