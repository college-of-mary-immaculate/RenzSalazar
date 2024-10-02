import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading
from PIL import Image, ImageTk

class CoffeeMaker:
    def __init__(self):
        self.water_level = 100
        self.coffee_beans = 100
        self.milk_level = 100

    def check_resources(self, cup_size):
        if self.water_level < cup_size * 0.7:
            return False, "Not enough water! Please refill."
        if self.coffee_beans < cup_size * 0.5:
            return False, "Not enough coffee beans! Please refill."
        if self.milk_level < (cup_size // 2) * 0.5:
            return False, "Not enough milk! Please refill."
        return True, ""

    def brew_coffee(self, coffee_type, strength, cup_size):
        can_brew, message = self.check_resources(cup_size)
        if not can_brew:
            return message

        app.update_image(None) 
        app.update_resource_labels()

        brew_time = (cup_size / 30) + 5  
        self.update_progress(0)
        for i in range(1, 101):
            time.sleep(brew_time / 100)
            self.update_progress(i)

        self.water_level -= cup_size * 0.7
        self.coffee_beans -= cup_size * 0.5
        if coffee_type in ["latte", "cappuccino"]:
            self.milk_level -= (cup_size // 2) * 0.5

        app.show_coffee_cup()  
        return f"Your {strength} {coffee_type} coffee is ready! Enjoy!"

    def update_progress(self, value):
        app.progress_var.set(value)
        app.root.update_idletasks()

    def refill_resources(self):
        threading.Thread(target=self.animate_refill).start()

    def animate_refill(self):
        total_time = 30 
        time_per_resource = total_time / 3 

        while self.water_level < 100:
            time.sleep(time_per_resource / 100)
            self.water_level += 1
            if self.water_level > 100:
                self.water_level = 100
            self.update_resource_labels()

        while self.coffee_beans < 100:
            time.sleep(time_per_resource / 100)
            self.coffee_beans += 1
            if self.coffee_beans > 100:
                self.coffee_beans = 100
            self.update_resource_labels()

        while self.milk_level < 100:
            time.sleep(time_per_resource / 100)
            self.milk_level += 1
            if self.milk_level > 100:
                self.milk_level = 100
            self.update_resource_labels()

    def update_resource_labels(self):
        app.water_level_label.config(text=f"Water Level: {self.water_level}%")
        app.coffee_level_label.config(text=f"Coffee Level: {self.coffee_beans}%")
        app.milk_level_label.config(text=f"Milk Level: {self.milk_level}%")

class CoffeeMakerApp:
    def __init__(self, root):
        self.coffee_maker = CoffeeMaker()
        self.root = root
        self.root.title("Coffee Maker")
        self.background_image = None
        self.image_label = None
        self.coffee_cup_image = None
        self.load_images()
        self.create_widgets()

    def load_images(self):
        background_image_path = "C:\\Users\\Acer\\Downloads\\background.jpg"

        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path).resize((800, 600)))

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(x=50, y=50)

        self.image_label = tk.Label(frame, bg='#f0f0f0', fg='white')
        self.image_label.grid(row=0, column=1, rowspan=10)

        self.coffee_type_var = tk.StringVar(value="espresso")
        tk.Label(frame, text="Select Coffee Type:", font=("Arial", 14), bg='#f0f0f0', fg='black').grid(row=0, column=0, sticky='w')
        tk.Radiobutton(frame, text="Espresso", variable=self.coffee_type_var, value="espresso", bg='#f0f0f0', fg='black').grid(row=1, column=0, sticky='w')
        tk.Radiobutton(frame, text="Latte", variable=self.coffee_type_var, value="latte", bg='#f0f0f0', fg='black').grid(row=2, column=0, sticky='w')
        tk.Radiobutton(frame, text="Cappuccino", variable=self.coffee_type_var, value="cappuccino", bg='#f0f0f0', fg='black').grid(row=3, column=0, sticky='w')

        self.strength_var = tk.StringVar(value="medium")
        tk.Label(frame, text="Select Coffee Strength:", font=("Arial", 14), bg='#f0f0f0', fg='black').grid(row=4, column=0, sticky='w')
        tk.Radiobutton(frame, text="Mild", variable=self.strength_var, value="mild", bg='#f0f0f0', fg='black').grid(row=5, column=0, sticky='w')
        tk.Radiobutton(frame, text="Medium", variable=self.strength_var, value="medium", bg='#f0f0f0', fg='black').grid(row=6, column=0, sticky='w')
        tk.Radiobutton(frame, text="Strong", variable=self.strength_var, value="strong", bg='#f0f0f0', fg='black').grid(row=7, column=0, sticky='w')

        tk.Label(frame, text="Enter Cup Size (ml):", font=("Arial", 14), bg='#f0f0f0', fg='black').grid(row=8, column=0, sticky='w')
        self.cup_size_entry = tk.Entry(frame, bg='white')
        self.cup_size_entry.grid(row=9, column=0, sticky='w')

        self.brew_button = tk.Button(frame, text="Brew Coffee", command=self.brew_coffee, bg='lightgreen')
        self.brew_button.grid(row=10, column=0, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=11, column=0, sticky='ew')

        self.result_label = tk.Label(frame, text="", font=("Arial", 12), bg='#f0f0f0', fg='black')
        self.result_label.grid(row=12, column=0)

        self.water_level_label = tk.Label(frame, text=f"Water Level: {self.coffee_maker.water_level}%", font=("Arial", 12), bg='#f0f0f0', fg='black')
        self.water_level_label.grid(row=13, column=0, sticky='w')

        self.coffee_level_label = tk.Label(frame, text=f"Coffee Level: {self.coffee_maker.coffee_beans}%", font=("Arial", 12), bg='#f0f0f0', fg='black')
        self.coffee_level_label.grid(row=14, column=0, sticky='w')

        self.milk_level_label = tk.Label(frame, text=f"Milk Level: {self.coffee_maker.milk_level}%", font=("Arial", 12), bg='#f0f0f0', fg='black')
        self.milk_level_label.grid(row=15, column=0, sticky='w')

        self.refill_button = tk.Button(frame, text="Refill Resources", command=self.refill_resources, bg='lightblue')
        self.refill_button.grid(row=16, column=0, pady=10)

    def update_image(self, image):
        if image:
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            self.image_label.config(image='')

    def show_coffee_cup(self):
        self.image_label.config(image=self.coffee_cup_image)
        self.image_label.image = self.coffee_cup_image

    def brew_coffee(self):
        coffee_type = self.coffee_type_var.get()
        strength = self.strength_var.get()
        try:
            cup_size = int(self.cup_size_entry.get())
            message = self.coffee_maker.brew_coffee(coffee_type, strength, cup_size)
            self.result_label.config(text=message)
            self.update_resource_labels()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid cup size.")

    def refill_resources(self):
        self.coffee_maker.refill_resources()

    def update_resource_labels(self):
        self.water_level_label.config(text=f"Water Level: {self.coffee_maker.water_level}%")
        self.coffee_level_label.config(text=f"Coffee Level: {self.coffee_maker.coffee_beans}%")
        self.milk_level_label.config(text=f"Milk Level: {self.coffee_maker.milk_level}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeMakerApp(root)
    root.mainloop()
