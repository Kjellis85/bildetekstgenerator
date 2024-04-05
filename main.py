# main.py

import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk
from ttkthemes import ThemedTk
from bildetekstgenerator_funksjoner import (
    load_image,
    add_text_to_image,
    save_image,
    scale_image_for_preview,
    process_image,
    color_mapping  # Antar at color_mapping er definert i bildetekstgenerator_funksjoner.py
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
    scale_thickness = 4
    font_size = int(font_size_var.get())
    text_color_name = text_color_var.get()
    text_color = color_mapping[text_color_name]  # Konverter til teknisk farge
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
    scale_positions = ['Venstre', 'Midtstilt', 'Høyre']
    scale_position_var = StringVar(value=scale_positions[1])  # Standardverdien er 'Midtstilt'
    scrollbar = ttk.Scrollbar(root)
    # Ordbok for å mappe brukervennlige fargenavn til tekniske fargenavn
    color_mapping = {'Hvit': 'white', 'Sort': 'black'}
    text_color_var = StringVar(value='Hvit')  # Standardverdien er 'Hvit'

    root.geometry('800x600')

    # Hovedframe for bilde og kontroller
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Frame for bildet
    image_frame = ttk.Frame(main_frame)
    image_frame.pack(side=LEFT, fill=BOTH, expand=True)

    image_label = Label(image_frame)
    image_label.pack(fill=BOTH, expand=True)

    # Frame for listen med bilder og knapper
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(side=LEFT, fill=Y)

    # Frame for listen med bilder
    list_frame = ttk.Frame(control_frame)
    list_frame.pack(fill=BOTH, expand=True)

    image_list_label = ttk.Label(list_frame, text="Lastede bilder:")
    image_list_label.pack()
    image_list = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set, show="tree")
    scrollbar.configure(command=image_list.yview)

    scrollbar.pack(side=RIGHT, fill=Y)
    image_list.pack(side=LEFT, fill=BOTH, expand=True)
    image_list.bind('<ButtonRelease-1>', on_image_select)

    # Frame for knapper og innstillinger
    button_frame = ttk.Frame(control_frame)
    button_frame.pack(fill=X)

    # Knapper fordelt på to kolonner
    button_columns = ttk.Frame(button_frame)
    button_columns.pack()

    # Konfigurer grid for å gi lik høyde til rader
    button_columns.grid_rowconfigure(0, weight=1)
    button_columns.grid_rowconfigure(1, weight=1)
    button_columns.grid_rowconfigure(2, weight=1)
    button_columns.grid_rowconfigure(3, weight=1)
    button_columns.grid_rowconfigure(4, weight=1)
    button_columns.grid_rowconfigure(5, weight=1)

    # Konfigurer grid for å gi lik bredde til kolonner
    button_columns.grid_columnconfigure(0, weight=1)
    button_columns.grid_columnconfigure(1, weight=1)

    # Første kolonne med knapper og labels
    button_column_1 = ttk.Frame(button_columns)
    button_column_1.grid(row=0, column=0, padx=(10, 5), pady=(5, 5), sticky="nsew")

    # Andre kolonne med knapper og OptionMenus
    button_column_2 = ttk.Frame(button_columns)
    button_column_2.grid(row=0, column=1, padx=(10, 5), pady=(5, 5), sticky="nsew")

    # Knapper og labels i kolonne 1, høyrejustert
    font_size_label = ttk.Label(button_column_1, text="Fontstørrelse:", anchor="se")
    font_size_label.grid(row=2, column=0, sticky="e", pady=11)

    text_color_label = ttk.Label(button_column_1, text="Tekstfarge:", anchor="se")
    text_color_label.grid(row=3, column=0, sticky="e", pady=11)

    position_label = ttk.Label(button_column_1, text="Tekstposisjon:", anchor="se")
    position_label.grid(row=4, column=0, sticky="e", pady=11)

    scale_position_label = ttk.Label(button_column_1, text="Målestokkposisjon:", anchor="se")
    scale_position_label.grid(row=5, column=0, sticky="e", pady=11)

    # OptionMenus i kolonne 2
    font_size_menu = ttk.OptionMenu(button_column_2, font_size_var, *map(str, font_sizes))
    font_size_menu.grid(row=2, column=1, sticky="ew")

    # Oppdater OptionMenu for tekstfarge til å bruke brukervennlige navn
    text_color_menu = ttk.OptionMenu(button_column_2, text_color_var, *color_mapping.keys())
    text_color_menu.grid(row=3, column=1, sticky="ew")

    position_select = ttk.OptionMenu(button_column_2, text_position_var, *text_positions)
    position_select.grid(row=4, column=1, sticky="ew")

    scale_position_menu = ttk.OptionMenu(button_column_2, scale_position_var, *scale_positions)
    scale_position_menu.grid(row=5, column=1, sticky="ew")

    # Knapper i kolonne 1 og 2, rad 1 og 2
    process_save_button = ttk.Button(button_column_1, text="Behandle og lagre bilder", command=process_and_save_images)
    process_save_button.grid(row=0, column=0, sticky="ew")

    text_button = ttk.Button(button_column_1,
                             text="Legg til tekst",
                             command=lambda:
                             add_text_to_image(image_label.filename,
                                               original_images, images,
                                               int(font_size_var.get()),
                                               text_position_var.get(),
                                               color_mapping[text_color_var.get()],  # Konverter til teknisk farge
                                               update_preview,
                                               "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf"))
    text_button.grid(row=1, column=0, sticky="ew")

    browse_button = ttk.Button(button_column_2, text="Last inn bilder", command=browse_files)
    browse_button.grid(row=0, column=1, sticky="ew")

    save_button = ttk.Button(button_column_2,
                         text="Lagre bilde",
                         command=lambda: save_image(image_label.filename, images, filedialog))
    save_button.grid(row=1, column=1, sticky="ew")


def main():
    global root, images
    root = ThemedTk(theme='adapta')
    root.title("Bilde Tekstlegger")
    images = {}
    setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()