import os
import qrcode
import json
import csv
from PIL import Image, ImageDraw, ImageFont


"""Program to crate the qr codes for the books in the library.
Eventually, this will go through the database and be automated 
--> new books? Entries without QRs?
"""

# ----- Setup -----
input_file = "data/all_lib_books.csv"
output_file_qrCodes = "book_qrCodes"
os.makedirs(output_file_qrCodes, exist_ok=True)
font_path = "C:\\Windows\\Fonts\\arial.ttf" #which font for PIL to use
font_size = 14

try:
    font = ImageFont.truetype(font_path,font_size)
except:
    font = ImageFont.load_default()

# ----- Process each book -----
with open(input_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = row['title'].strip()
        author = row['author'].strip()

        #encode as json for the qrcode
        data = json.dumps({"title": title, "author":author})
        qr_img = qrcode.make(data).convert("RGB")

        scale_factor = 0.7  # 0.5 = half size, 0.3 = 30%, etc.
        new_size = (int(qr_img.width * scale_factor), int(qr_img.height * scale_factor))
        qr_img = qr_img.resize(new_size, Image.Resampling.LANCZOS)

        #make a qr with space for text
        draw_area_h = 40
        new_width, new_height = qr_img.width, qr_img.height + draw_area_h
        combined = Image.new("RGB", (new_width,new_height), "white")
        combined.paste(qr_img,(0,0))

        #add text of title/author under the qr
        draw = ImageDraw.Draw(combined)
        text = f"{title} - {author}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = (new_width - text_w) // 2
        text_y = qr_img.height + (draw_area_h - text_h) // 2
        draw.text((text_x, text_y), text, fill='black', font=font)

        #save the file
        file_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = os.path.join(output_file_qrCodes, f"{file_title}.png")
        combined.save(filename)

        print(f"QR Created for '{title}' --> {filename}")

print("\n\nAll QR Codes generated!")