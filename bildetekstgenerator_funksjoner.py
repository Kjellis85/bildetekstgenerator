# bildetekstgenerator_funksjoner.py

import os
from PIL import Image, ImageFont, ImageDraw


def load_image(filename, images, original_images, update_preview, update_image_list):
    image = Image.open(filename)
    images[filename] = image
    original_images[filename] = image.copy()  # Lagre en kopi av det originale bildet
    update_preview(image, filename)  # Pass both image and filename
    update_image_list()


def add_text_to_image(filename, original_images, images, font_size, position, text_color, update_preview, font_path):
    if filename:
        # Bruk en kopi av det originale bildet uten tidligere påført tekst
        image = original_images[filename].copy()
        draw = ImageDraw.Draw(image)
        text = format_filename(filename)
        font = ImageFont.truetype(font_path, font_size)

        # Bruk getbbox for å beregne størrelsen på teksten
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Beregn posisjonen for teksten basert på valgt posisjon
        x, y = get_position(image, text_width, text_height, position)

        # Bruk den valgte tekstfargen
        draw.text((x, y), text, font=font, fill=text_color)

        # Oppdater bildet i ordboken med den nye teksten
        images[filename] = image
        update_preview(image, filename)  # Oppdater forhåndsvisningen med det skalerte bildet


def format_filename(filename):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    parts = name.split('_')
    if len(parts) >= 2:
        # Erstatt første understrek med punktum og fjern resten etter andre understrek
        formatted_name = parts[0] + '.' + parts[1].split('_')[0]
    else:
        # Hvis det bare er en del, bruk den som den er
        formatted_name = parts[0]
    return formatted_name


def get_position(image, text_width, text_height, position):
    w, h = image.size
    margin = 50  # Sett margin til 50 piksler
    positions = {
        'Venstre hjørne, oppe': (margin, margin),
        'Høyre hjørne, oppe': (w - text_width - margin, margin),
        'Venstre hjørne, nede': (margin, h - text_height - margin),
        'Høyre hjørne, nede': (w - text_width - margin, h - text_height - margin)
    }
    return positions[position]


def save_image(filename, images, filedialog):
    if filename:
        save_path = filedialog.asksaveasfilename(defaultextension=".tiff")
        if save_path:
            image = images[filename]
            image.save(save_path, format='TIFF', save_all=True)


def get_fonts(fonts_path):
    font_files = [f for f in os.listdir(fonts_path) if f.endswith('.ttf')]
    return font_files


def scale_image_for_preview(image, max_height=750):
    original_width, original_height = image.size
    if original_height > max_height:
        ratio = max_height / original_height
        new_width = int(original_width * ratio)
        image = image.resize((new_width, max_height), resample=Image.LANCZOS)
    return image
