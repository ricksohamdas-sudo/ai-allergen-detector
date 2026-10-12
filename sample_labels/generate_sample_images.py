"""
Generates clean mock product label images for demonstration.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from sample_data import SAMPLE_PRODUCTS

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_label_image(product: dict, filename: str):
    width, height = 750, 620
    img = Image.new("RGB", (width, height), color=(250, 252, 255))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, width, 85], fill=(30, 58, 138))
    
    # Try basic fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 16)
        font_head = ImageFont.truetype("arialbd.ttf", 18)
        font_text = ImageFont.truetype("arial.ttf", 15)
        font_badge = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_head = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    draw.text((25, 18), product["title"], fill=(255, 255, 255), font=font_title)
    draw.text((25, 52), f"Languages: {product['primary_language']} | FSSAI Compliance Verified", fill=(219, 234, 254), font=font_sub)

    # Body frame
    draw.rectangle([20, 105, width - 20, height - 25], outline=(203, 213, 225), width=2, fill=(255, 255, 255))

    # Badge for category
    draw.rectangle([35, 120, 260, 150], fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.text((45, 126), "FOOD INGREDIENT SPECIFICATION", fill=(67, 56, 202), font=font_badge)

    # Ingredients section
    y_pos = 165
    draw.text((35, y_pos), "INGREDIENTS / सामग्री / উপাদান:", fill=(30, 41, 59), font=font_head)
    y_pos += 28

    # Wrap label text roughly
    lines = product["label_text"].split("\n")
    for block in lines:
        if not block.strip():
            y_pos += 8
            continue
        words = block.split(" ")
        curr_line = ""
        for w in words:
            test_line = f"{curr_line} {w}".strip()
            if len(test_line) > 75:
                draw.text((35, y_pos), curr_line, fill=(51, 65, 85), font=font_text)
                y_pos += 22
                curr_line = w
            else:
                curr_line = test_line
        if curr_line:
            draw.text((35, y_pos), curr_line, fill=(51, 65, 85), font=font_text)
            y_pos += 22

    # Bottom seal
    draw.rectangle([35, height - 60, width - 35, height - 35], fill=(241, 245, 249))
    draw.text((50, height - 54), "AUTHENTIC PACKAGING REPLICA FOR AI OCR & ALLERGEN ANALYSIS", fill=(100, 116, 139), font=font_badge)

    filepath = os.path.join(OUT_DIR, filename)
    img.save(filepath, "JPEG", quality=92)
    return filepath

if __name__ == "__main__":
    for p in SAMPLE_PRODUCTS:
        fname = f"{p['id']}.jpg"
        out_path = create_label_image(p, fname)
        print(f"Generated: {out_path}")
