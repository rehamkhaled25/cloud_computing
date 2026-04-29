import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from config import COLORS
from utils import get_image

def load_local_image(path, size=None):
    try:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return None
            
        im = Image.open(path)
        if size:
            im = im.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(im)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS.get("bg_light", "#f7f7f7"))
        self.controller = controller
        self.images = []  # For PIL images
        self.img_refs = []  # For get_image references

        # --- Header ---
        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")
        
        # Back Button - connects to RestaurantPage
        tk.Button(header, text="← Back to Restaurants", 
                  font=("Arial", 10, "bold"), bg="white", fg="#666",
                  bd=0, cursor="hand2", 
                  command=lambda: controller.show_frame("RestaurantPage"),
                  activebackground="white", activeforeground="#FCC900").pack(side="left", padx=20)

        tk.Label(header, text="GoEats", bg="white", fg="#FCC900",
                 font=("Arial", 22, "bold")).pack(side="right", padx=30)

        # --- Menu Header ---
        tk.Label(self, text="Available Dishes",
                 bg="#eaeaea", font=("Arial", 14),
                 pady=10).pack(fill="x")

        # --- Main Grid ---
        main_container = tk.Frame(self, bg=COLORS.get("bg_light", "#f7f7f7"))
        main_container.pack(fill="both", expand=True)
        
        # Padding for centering
        tk.Frame(main_container, bg=COLORS.get("bg_light", "#f7f7f7"), width=40).pack(side="left", fill="y")
        center_frame = tk.Frame(main_container, bg=COLORS.get("bg_light", "#f7f7f7"))
        center_frame.pack(side="left", fill="both", expand=True)
        tk.Frame(main_container, bg=COLORS.get("bg_light", "#f7f7f7"), width=40).pack(side="right", fill="y")

        # Menu items with price as integer for consistency
        menu_items = [
            ("images/burger.png", "Classic Burger", 120),
            ("images/pizza.jpeg", "Pepperoni Pizza", 150),
            ("images/pasta.jpeg", "Red Pasta", 70),
            ("images/taco.webp", "Beef Taco", 100),
            ("images/kofta.jpeg", "Beef Kofta", 130),
            ("images/noodles.jpg", "Garlic Noodles", 80),
            ("images/shawarma.jpg", "Shawarma", 140),
            ("images/tart.jpg", "Tart", 65),
            ("images/cheesecake.webp", "Cheesecake", 70),
            ("images/soda.jpeg", "Soda", 25),
        ]

        grid_frame = tk.Frame(center_frame, bg=COLORS.get("bg_light", "#f7f7f7"))
        grid_frame.pack(pady=20)

        cols = 5
        for i, (path, name, price) in enumerate(menu_items):
            row = i // cols
            col = i % cols

            card = tk.Frame(grid_frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Try to load image using get_image first (from utils)
            img = get_image(path, (160, 110))
            if img:
                self.img_refs.append(img)
                tk.Label(card, image=img, bg="white").pack(pady=5)
            else:
                # Fallback to local loading
                img_local = load_local_image(path, (160, 110))
                if img_local:
                    self.images.append(img_local)
                    tk.Label(card, image=img_local, bg="white").pack(pady=5)
                else:
                    tk.Label(card, text="Image Not Found", bg="#eee", width=20, height=6, font=("Arial", 8)).pack(pady=5)

            tk.Label(card, text=name, bg="white", font=("Arial", 10, "bold")).pack()
            tk.Label(card, text=f"EGP {price}", bg="white", fg="#FCC900", font=("Arial", 10, "bold")).pack(pady=2)

           
            tk.Button(card, text="View Details",
                      bg="#FCC900", fg="white",
                      font=("Arial", 8, "bold"),
                      bd=0, padx=10, pady=5,
                      cursor="hand2",
                      command=lambda n=name, p=price: self.open_details(n, p)).pack(pady=(5, 10))

        # --- Footer ---
        footer = tk.Frame(self, bg="#f0f0f0", height=40)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2026 otlobly | Fresh Food Delivered",
                 bg="#f0f0f0", fg="#666", font=("Arial", 9)).pack(pady=10)

    def open_details(self, name, price):
        """Navigate to item details page with selected item"""
        # Check if ItemDetailsPage exists in controller frames
        if "ItemDetailsPage" in self.controller.frames:
           
            if hasattr(self.controller.frames["ItemDetailsPage"], "set_item"):
                self.controller.frames["ItemDetailsPage"].set_item(name, price)
            self.controller.show_frame("ItemDetailsPage")
        else:
            print(f"Opening details for: {name} - EGP {price}")
           
            from tkinter import messagebox
            messagebox.showinfo("Item Details", f"{name}\nPrice: EGP {price}\n\nCustomization options coming soon!")

    def go_home(self):
     
        self.controller.show_frame("RestaurantPage")