# main.py

import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from bildetekstgenerator_funksjoner import (
    load_image,
    add_text_to_image,
    save_image,
    save_all_images,
    scale_image_for_preview
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
    tk_image = ImageTk.PhotoImage(scale_image_for_preview(image))
    image_label.config(image=tk_image)
    image_label.image = tk_image
    image_label.filename = filename


def setup_gui(root):
    global image_label, font_size_var, position, image_list, text_color_var
    font_sizes = [30, 36, 42, 54, 78]  # Definer listen med fontstørrelser
    font_size_var = StringVar(value='42')  # Sett standardverdien til '42' som en streng
    position = StringVar(value='Venstre hjørne, oppe')
    text_color_var = StringVar(value='white')  # Standardverdien er hvit

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

    save_all_button = Button(button_frame, text="Lagre alle bilder", command=lambda: save_all_images(
        original_images, images, int(font_size_var.get()), position.get(), text_color_var.get(),
        "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf", filedialog))
    save_all_button.pack(side=LEFT)

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
    position_select = OptionMenu(button_frame, position, 'Venstre hjørne, oppe', 'Høyre hjørne, oppe', 'Venstre hjørne, nede', 'Høyre hjørne, nede')
    position_select.pack(side=LEFT)

    text_button = Button(button_frame, text="Legg til tekst",
                         command=lambda: add_text_to_image(image_label.filename, original_images, images,
                                                           int(font_size_var.get()),
                                                           position.get(), text_color_var.get(), update_preview,
                                                           "D:/Python prosjekter/bildetekstgenerator/Fonts/OpenSans_Light.ttf"))
    text_button.pack(side=LEFT)

    save_button = Button(button_frame, text="Lagre bilde", command=lambda: save_image(image_label.filename, images, filedialog))
    save_button.pack(side=LEFT)

    browse_button = Button(button_frame, text="Last inn bilder", command=browse_files)
    browse_button.pack(side=LEFT)


def main():
    global root, images
    root = Tk()
    root.title("Bilde Tekstlegger")
    images = {}
    setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
