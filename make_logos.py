import math, os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('static/images', exist_ok=True)

def create_logo(output_path, dark_mode=False):
    width, height = 900, 240
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy, r = 120, 120, 75

    for i in range(r, 0, -1):
        ratio = i / r
        if not dark_mode:
            red, green, blue = int(79 + (99 - 79) * (1 - ratio)), int(70 + (102 - 70) * (1 - ratio)), int(229 + (241 - 229) * (1 - ratio))
        else:
            red, green, blue = int(129 + (165 - 129) * (1 - ratio)), int(140 + (180 - 140) * (1 - ratio)), int(248 + (252 - 248) * (1 - ratio))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(red, green, blue, 255))

    for t in range(0, 360, 2):
        rad = math.radians(t)
        ox = cx + int(95 * math.cos(rad))
        oy = cy + int(35 * math.sin(rad) * math.cos(math.radians(35)) - 95 * math.cos(rad) * math.sin(math.radians(35)))
        color = (255, 255, 255, 200) if not dark_mode else (220, 230, 255, 220)
        draw.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=color)

    try:
        font_main = ImageFont.truetype('arialbd.ttf', 68)
        font_sub = ImageFont.truetype('arial.ttf', 22)
    except:
        font_main = font_sub = ImageFont.load_default()

    text_color = (26, 32, 44, 255) if not dark_mode else (255, 255, 255, 255)
    sub_color = (100, 116, 139, 255) if not dark_mode else (203, 213, 225, 255)
    accent_color = (79, 70, 229, 255) if not dark_mode else (129, 140, 248, 255)

    draw.text((230, 60), 'STYLE', font=font_main, fill=text_color)
    draw.text((490, 60), 'SPHERE', font=font_main, fill=accent_color)
    draw.text((235, 145), 'C U R A T E D   L I F E S T Y L E', font=font_sub, fill=sub_color)

    img.save(output_path, 'PNG')
    print('Generated:', output_path)

create_logo('static/images/stylesphere_logo_primary.png', dark_mode=False)
create_logo('static/images/stylesphere_logo_white.png', dark_mode=True)
