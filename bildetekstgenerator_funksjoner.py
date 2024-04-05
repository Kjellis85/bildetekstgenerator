# bildetekstgenerator_funksjoner.py

from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import cv2
import os
import numpy as np

color_mapping= {'Hvit': 'white', 'Sort': 'black'}

def load_image(filename, images, original_images, update_preview, update_image_list):
    image = Image.open(filename)
    images[filename] = image
    original_images[filename] = image.copy()  # Lagre en kopi av det originale bildet
    update_preview(image, filename)  # Pass both image and filename
    update_image_list()


def add_text_to_image(filename, original_images, images, font_size, position, text_color_name, update_preview, font_path):
    text_color = color_mapping[text_color_name]

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
    width, height = image.size
    margin = 50  # Sett margin til 50 piksler
    positions = {
        'Venstre hjørne, oppe': (margin, margin),
        'Høyre hjørne, oppe': (width - text_width - margin, margin),
        'Venstre hjørne, nede': (margin, height - text_height - margin),
        'Høyre hjørne, nede': (width - text_width - margin, height - text_height - margin)
    }
    return positions[position]


def save_image(filename, images, filedialog):
    if filename:
        save_path = filedialog.asksaveasfilename(defaultextension=".tiff")
        if save_path:
            image = images[filename]
            image.save(save_path, format='TIFF', save_all=True)


def save_all_images(original_images, scale_thickness, font_size, text_color, font_path, position, filedialog):
    # Be brukeren om en mappe for å lagre alle bildene
    directory = filedialog.askdirectory()
    if not directory:  # Hvis brukeren avbryter, avslutt funksjonen
        return

    for filename in original_images:
        try:
            # Lag en kopi av det originale bildet
            image = original_images[filename].copy()
            # Behandle bildet og legg til målestokk
            processed_image = process_image(image, scale_thickness, font_size, text_color, position)
            # Legg til tekst basert på filnavnet
            draw = ImageDraw.Draw(processed_image)
            text = format_filename(filename)
            font = ImageFont.truetype(font_path, font_size)
            # Beregn posisjon og størrelse for teksten
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x, y = get_position(processed_image, text_width, text_height, position)
            # Tegn teksten på bildet
            draw.text((x, y), text, font=font, fill=text_color)
            # Lagre bildet i den valgte mappen
            save_path = os.path.join(directory, os.path.basename(filename))
            processed_image.save(save_path, format='TIFF', save_all=True)
        except Exception as e:
            print(f"En feil oppstod ved behandling av bildet {filename}: {e}")


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


# Funksjon for å laste inn og behandle bilder
def process_image(image, scale_thickness, font_size, text_color, scale_position, text_position, filename, font_path):
    # Konverter bildet til et format som OpenCV kan jobbe med
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Dekod QR-koden for å finne målestokkens lengde
    decoded_objects = decode(image_cv)
    for obj in decoded_objects:
        # Anta at QR-koden inneholder informasjon om målestokken i mm
        scale_length_mm = int(obj.data.decode())
        # Finn bredden av QR-koden i piksler
        qr_code_width_px = obj.rect.width
        # Regn ut målestokken i piksler basert på antall mm
        scale_length_px = (scale_length_mm / 100) * qr_code_width_px
        # Tegn målestokken på bildet
        draw_scale(image, scale_length_px, scale_thickness, font_size, scale_length_mm, text_color, scale_position)

    # Legg til tekst basert på filnavnet
    draw = ImageDraw.Draw(image)
    text = format_filename(filename)
    font = ImageFont.truetype(font_path, font_size)
    # Beregn posisjon og størrelse for teksten
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x, y = get_position(image, text_width, text_height, text_position)
    # Tegn teksten på bildet
    draw.text((x, y), text, font=font, fill=text_color)

    return image

# Funksjon for å tegne målestokken på bildet
def draw_scale(image, scale_length_px, scale_thickness, font_size, scale_length_mm, text_color, scale_position):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    margin = 50  # Margin fra kanten av bildet

    # Beregn start_x basert på valgt posisjon
    if scale_position == 'Venstre':
        start_x = margin
    elif scale_position == 'Midtstilt':
        start_x = (width - scale_length_px) // 2
    elif scale_position == 'Høyre':
        start_x = width - scale_length_px - margin
    else:
        raise ValueError("Ugyldig posisjon valgt. Velg mellom 'venstre', 'midt', eller 'høyre'.")

    # Topp-posisjonen for målestokken
    top_of_scale = height - (margin * 3) - scale_thickness
    # Bunnen av målestokken
    bottom_of_scale = top_of_scale + scale_thickness

    # Tegn målestokken
    draw.rectangle([start_x, top_of_scale, start_x + scale_length_px, bottom_of_scale], fill=text_color)

    # Legg til tekst
    font_path = "D:/Python prosjekter/QR_kodeleser/Fonts/OpenSans_Light.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = f"{scale_length_mm / 100} cm"

    # Bruk textlength for å få bredden på teksten
    text_width = draw.textlength(text, font=font) / 64.0  # Konverter fra 1/64 piksler til piksler

    # Beregn x-posisjonen for teksten basert på valgt posisjon
    text_x = start_x  # Starten på teksten er lik starten på målestokken for alle posisjoner

    # Beregn y-posisjonen for teksten
    bbox = draw.textbbox((0, 0), text, font=font)
    text_height = bbox[3] - bbox[1]

    # Teksten ligger 25 piksler over toppen av målestokken
    text_y = bottom_of_scale + (margin/4)
    draw.text((text_x, text_y), text, font=font, fill=text_color)
