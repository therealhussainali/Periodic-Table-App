import tkinter as tk
from PIL import Image, ImageTk
import periodictable
from element_data import get_element_data

class PeriodicTableGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Periodic Table")
        
        self.elements = get_element_data()
        self.element_images = []

        self.create_periodic_table()

    def create_periodic_table(self):
        for element_data in self.elements:
            element_frame = tk.Frame(self.master, bg="#3498db", bd=2, relief=tk.RAISED)
            element_frame.grid(row=element_data["row"], column=element_data["column"], padx=2, pady=2, sticky="nsew")

            tk.Label(element_frame, text=str(element_data["atomicNumber"]), font=("Arial", 8), bg="#3498db", fg="white").grid(row=0, column=0, sticky="w")
            tk.Label(element_frame, text=element_data["symbol"], font=("Arial", 12, "bold"), bg="#3498db", fg="white").grid(row=1, column=0)
            tk.Label(element_frame, text=element_data["name"], font=("Arial", 8), bg="#3498db", fg="white").grid(row=2, column=0, sticky="w")

            element_frame.bind("<Button-1>", lambda event, el=element_data: self.show_element_popup(el))

        # Uniform row and column weights for proper resizing
        for i in range(1, 11):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def load_element_image(self, name):
        try:
            image_path = f"element_images/{name.lower()}.jpg"  # Assuming images are named as name.jpg
            element_image = Image.open(image_path)
            return ImageTk.PhotoImage(element_image)
        except FileNotFoundError:
            return None

    def resize_image(self, image, size, name):
        if image:
            pil_image = Image.open(f"element_images/{name.lower()}.jpg")  # Open the image again
            pil_image = pil_image.resize(size)
            return ImageTk.PhotoImage(pil_image)
        return None

    def show_element_popup(self, element_data):
        element_image = self.load_element_image(element_data["name"].lower())
        resized_image = self.resize_image(element_image, (150, 150), element_data["name"].lower())
        self.element_images.append(resized_image)

        element_atomic_number = element_data["atomicNumber"]
        element_mass = periodictable.elements[element_atomic_number].mass

        popup_text = f"Atomic Number: {element_atomic_number}\nSymbol: {element_data['symbol']}\nName: {element_data['name']}\nMass: {element_mass} u"

        popup = tk.Toplevel(self.master)
        popup.title(f"Element Details - {element_data['name']}")

        popup.geometry("400x300")  # Set the size of the popup window

        if resized_image:
            image_label = tk.Label(popup, image=resized_image)
            image_label.grid(row=0, column=0, pady=10)

        text_label = tk.Label(popup, text=popup_text, font=("Arial", 12))
        text_label.grid(row=1, column=0, pady=(0, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = PeriodicTableGUI(root)
    root.mainloop()
