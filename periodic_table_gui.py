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
            element_frame = tk.Frame(self.master, bg=self.get_element_color(element_data["category"]), bd=2, relief=tk.RAISED)
            element_frame.grid(row=element_data["row"], column=element_data["column"], padx=2, pady=2, sticky="nsew")

            tk.Label(element_frame, text=str(element_data["atomicNumber"]), font=("Arial", 10), bg=element_frame.cget("bg")).grid(row=0, column=0, sticky="w")
            tk.Label(element_frame, text=element_data["symbol"], font=("Arial", 12, "bold"), bg=element_frame.cget("bg")).grid(row=1, column=0)
            tk.Label(element_frame, text=element_data["name"], font=("Arial", 8), bg=element_frame.cget("bg")).grid(row=2, column=0, sticky="w")


            element_frame.bind("<Button-1>", lambda event, el=element_data: self.show_element_popup(el))

        # Uniform row and column weights for proper resizing
        for i in range(18):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)
        
        legend_frame = tk.Frame(self.master)
        legend_frame.grid(row=10, column=17,rowspan=8,columnspan=2, sticky="se", padx=10, pady=10)

        legend_title = tk.Label(legend_frame, text="Legend", font=("Arial", 12, "bold"))
        legend_title.grid(row=0, column=0, columnspan=2)

        classifications = [
            "Alkali Metal", "Alkaline Earth Metal", "Transition Metal",
            "Post-Transition Metal", "Metalloid", "Reactive Non-Metal",
            "Noble Gas", "Lanthanide", "Actinide"
        ]

        legend_colors = [
            "#FFD700",  # Gold
            "#90EE90",  # Light Green
            "#ADD8E6",  # Light Blue
            "#FFA07A",  # Light Salmon
            "#D3D3D3",  # Light Gray
            "#FF6347",  # Tomato
            "#87CEEB",  # Sky Blue
            "#DA70D6",  # Orchid
            "#8A2BE2"   # Blue Violet
        ]

        for i, classification in enumerate(classifications):
            tk.Label(legend_frame, text=classification, bg=legend_colors[i]).grid(row=i + 1, column=0, pady=5, padx=5, sticky="w")

        self.master.grid_rowconfigure(10, weight=0)
        self.master.grid_columnconfigure(17, weight=0)

    def get_element_color(self, category):
        # Assigning colors based on element group
        group_colors = {
            "Alkali Metal": "#FFD700",        # Gold
            "Alkaline Earth Metal": "#90EE90", # Light Green
            "Transition Metal": "#ADD8E6",     # Light Blue
            "Post-Transition Metal": "#FFA07A", # Light Salmon
            "Metalloid": "#D3D3D3",           # Light Gray
            "Reactive Non-Metal": "#FF6347",   # Tomato
            "Noble Gas": "#87CEEB",            # Sky Blue
            "Lanthanide": "#DA70D6",          # Orchid
            "Actinide": "#8A2BE2"              # Blue Violet
        }

        return group_colors.get(category, "#FFFFFF")  # Default to white for unknown categories

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
