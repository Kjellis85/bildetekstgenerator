# main.py

import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk
from bildetekstgenerator_funksjoner import (
    load_image,
    add_text_to_image,
    save_image,
    scale_image_for_preview,
    process_image
)


def on_image_select(event):
    w = event.widget
    index = int(w.curselection()[0])
    filename = list(images.keys())[index]
    image = images[filename]
    update_preview(image, filename)


def update_image_list():
    image_list.delete(0, END)
    for filename in images.keys():
        image_list.insert(END, os.path.basename(filename))


original_images = {}  # Ordbok for å holde de originale bildene uten tekst


def browse_files():
    filetypes = (
        ('JPEG files', '*.jpg'),
        ('TIFF files', '*.tiff *tif'),
        ('All files', '*.*')
    )
    filenames = filedialog.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)
    for filename in filenames:
        load_image(filename, images, original_images, update_preview, update_image_list)


def update_preview(image, filename):
    scale_thickness = 4  # Du kan endre dette til å være en brukerdefinert verdi om nødvendig
    font_size = int(font_size_var.get())
    text_color = text_color_var.get()
    scale_position = scale_position_var.get()
    text_position = text_position_var.get()
    font_path = "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf"

    # Lag en kopi av bildet for forhåndsvisning
    preview_image = image.copy()
    # Tegn målestokken på forhåndsvisningsbildet
    preview_image = process_image(preview_image, scale_thickness, font_size, text_color, scale_position, text_position, filename, font_path)
    # Skaler bildet for forhåndsvisning
    tk_image = ImageTk.PhotoImage(scale_image_for_preview(preview_image))
    image_label.config(image=tk_image)
    image_label.image = tk_image
    image_label.filename = filename

def process_and_save_images():
    if not original_images:
        messagebox.showerror("Error", "Ingen bilder er lastet inn.")
        return

    # La brukeren velge hvor de bearbeidede bildene skal lagres
    save_directory = filedialog.askdirectory(title='Velg mappen for å lagre bearbeidede bilder')
    if not save_directory:
        messagebox.showerror("Error", "Ingen mappe ble valgt for lagring.")
        return

    scale_position = scale_position_var.get()  # Hent posisjonen for målestokken fra GUI-komponenten
    text_position = text_position_var.get()  # Hent posisjonen for teksten fra GUI-komponenten
    scale_thickness = 4  # Du kan endre dette til å være en brukerdefinert verdi om nødvendig
    font_size = int(font_size_var.get())
    text_color = text_color_var.get()
    font_path = "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf"  # Endre til din faktiske font-path

    for filename, image in original_images.items():
        try:
            # Behandle hvert bilde og legg til målestokk og tekst
            processed_image = process_image(image, scale_thickness, font_size, text_color, scale_position,
                                            text_position, filename, font_path)
            # Lagre det bearbeidede bildet uten å endre filnavnet
            save_path = os.path.join(save_directory, os.path.basename(filename))
            processed_image.save(save_path)
        except Exception as e:
            messagebox.showerror("Error", f"En feil oppstod ved behandling av bildet {filename}: {e}")

    messagebox.showinfo("Suksess", "Alle bildene har blitt behandlet og lagret.")

def setup_gui(root):
    global image_label, font_size_var, text_position_var, image_list, text_color_var, scale_position_var
    font_sizes = [30, 36, 42, 54, 78]  # Definer listen med fontstørrelser
    font_size_var = StringVar(value='78')  # Sett standardverdien til '78' som en streng
    text_positions = ['Venstre hjørne, oppe', 'Høyre hjørne, oppe', 'Venstre hjørne, nede', 'Høyre hjørne, nede']
    text_position_var = StringVar(value=text_positions[0])  # Standardverdien er 'Venstre hjørne, oppe'
    text_color_var = StringVar(value='white')  # Standardverdien er hvit
    scale_positions = ['Venstre', 'Midtstilt', 'Høyre']
    scale_position_var = StringVar(value=scale_positions[1])  # Standardverdien er 'Midtstilt'

    # Hovedframe for bilde og kontroller
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True, pady=20)

    # Frame for bildet
    image_frame = Frame(main_frame)
    image_frame.pack(side=LEFT, fill=BOTH, expand=True)

    image_label = Label(image_frame)
    image_label.pack()

    # Frame for listen med bilder og knapper
    control_frame = Frame(main_frame)
    control_frame.pack(side=LEFT, fill=Y)

    # Frame for listen med bilder
    list_frame = Frame(control_frame)
    list_frame.pack(fill=BOTH, expand=True)

    image_list_label = Label(list_frame, text="Lastede bilder:")
    image_list_label.pack()
    image_list = Listbox(list_frame)
    image_list.pack(fill=BOTH, expand=True)
    image_list.bind('<<ListboxSelect>>', on_image_select)

    # Frame for knapper og innstillinger
    button_frame = Frame(control_frame)
    button_frame.pack(fill=X)

    process_save_button = Button(button_frame, text="Behandle og lagre bilder", command=process_and_save_images)
    process_save_button.pack(side=LEFT)

    font_size_label = Label(button_frame, text="Fontstørrelse:")
    font_size_label.pack(side=LEFT)
    font_size_menu = OptionMenu(button_frame, font_size_var, *map(str, font_sizes))
    font_size_menu.pack(side=LEFT)

    text_color_label = Label(button_frame, text="Tekstfarge:")
    text_color_label.pack(side=LEFT)
    text_color_menu = OptionMenu(button_frame, text_color_var, 'white', 'black')
    text_color_menu.pack(side=LEFT)

    position_label = Label(button_frame, text="Tekstposisjon:")
    position_label.pack(side=LEFT)
    position_select = OptionMenu(button_frame, text_position_var, *text_positions)
    position_select.pack(side=LEFT)

    text_button = Button(button_frame, text="Legg til tekst",
                         command=lambda: add_text_to_image(image_label.filename, original_images, images,
                                                           int(font_size_var.get()),
                                                           text_position_var.get(), text_color_var.get(), update_preview,
                                                           "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf"))
    text_button.pack(side=LEFT)

    save_button = Button(button_frame, text="Lagre bilde", command=lambda: save_image(image_label.filename, images, filedialog))
    save_button.pack(side=LEFT)

    browse_button = Button(button_frame, text="Last inn bilder", command=browse_files)
    browse_button.pack(side=LEFT)

    scale_position_label = Label(button_frame, text="Målestokkposisjon:")
    scale_position_label.pack(side=LEFT)
    scale_position_menu = OptionMenu(button_frame, scale_position_var, *scale_positions)
    scale_position_menu.pack(side=LEFT)


def main():
    global root, images
    root = Tk()
    root.title("Bilde Tekstlegger")
    images = {}
    setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()