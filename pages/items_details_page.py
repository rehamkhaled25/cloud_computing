import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from config import COLORS

def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

class ItemDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.base_price = 0
        self.quantity = 1
        self.item_name = ""
        self.size_prices = {"Small": 0, "Medium": 10, "Large": 20}
        self.extras_data = [("Cheese", 5), ("Fries", 10), ("Mushroom", 7)]
        self.setup_ui()
    
    def setup_ui(self):
        self.img = None
        
        # Header with back button
        header = tk.Frame(self, bg="#f2f2f2")
        header.pack(fill="x", padx=10, pady=(10, 0))
        tk.Button(header, text="← Back", bg="#FCC900", fg="white", bd=0,
                 padx=15, pady=5, command=self.go_back).pack(side="left")
        
        # Image
        self.image_label = tk.Label(self, bg="#e0e0e0")
        self.image_label.pack()
        
        # Main card
        card = tk.Frame(self, bg="white")
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top row
        top_row = tk.Frame(card, bg="white")
        top_row.pack(fill="x", padx=15, pady=(10, 0))
        self.name_label = tk.Label(top_row, font=("Arial", 16), bg="white")
        self.name_label.pack(side="left")
        
        # Quantity controls
        qty_frame = tk.Frame(top_row, bg="white")
        qty_frame.pack(side="right")
        tk.Button(qty_frame, text="-", width=2, bg="#FCC900", fg="white",
                 bd=0, command=self.decrease).pack(side="left")
        self.qty_label = tk.Label(qty_frame, text="1", font=("Arial", 12),
                                 width=3, bg="white")
        self.qty_label.pack(side="left")
        tk.Button(qty_frame, text="+", width=2, bg="#FCC900", fg="white",
                 bd=0, command=self.increase).pack(side="left")
        
        # Description
        self.desc_label = tk.Label(card, font=("Arial", 10), fg="#777", bg="white")
        self.desc_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Size selection
        tk.Label(card, text="Choose Size", font=("Arial", 12), bg="white"
                ).pack(anchor="w", padx=15)
        self.size = tk.StringVar(value="Medium")
        for size, price in self.size_prices.items():
            tk.Radiobutton(card, text=f"{size} (+{price})", variable=self.size,
                          value=size, indicatoron=False, bg="white",
                          selectcolor="#FCC900", command=self.update_price
                          ).pack(anchor="w", padx=25, fill="x")
        
        # Extras
        tk.Label(card, text="Extras", font=("Arial", 12), bg="white"
                ).pack(anchor="w", padx=15, pady=(10, 0))
        self.extra_vars = []
        for name, price in self.extras_data:
            v = tk.IntVar()
            tk.Checkbutton(card, text=f"{name} (+{price})", variable=v,
                          indicatoron=False, bg="white", selectcolor="#FCC900",
                          command=self.update_price).pack(anchor="w", padx=25, fill="x")
            self.extra_vars.append((v, price))
        
        # Instructions
        tk.Label(card, text="Special Instructions", font=("Arial", 12), bg="white"
                ).pack(anchor="w", padx=15, pady=(10, 0))
        self.notes = tk.Text(card, height=3, bd=1, relief="solid")
        self.notes.pack(fill="x", padx=15, pady=5)
        
        # Bottom
        bottom = tk.Frame(card, bg="white")
        bottom.pack(fill="x", padx=15, pady=15)
        self.price_label = tk.Label(bottom, font=("Arial", 14), fg="#FCC900", bg="white")
        self.price_label.pack(side="left")
        tk.Button(bottom, text="Add to Cart", bg="#FCC900", fg="white",
                 bd=0, padx=20, pady=10, command=self.add_to_cart).pack(side="right")
    
    def go_back(self):
        self.controller.show_frame("MenuPage")
    
    def set_item(self, name, price):
        self.item_name = name
        self.base_price = price
        self.quantity = 1
        self.qty_label.config(text="1")
        self.name_label.config(text=name)
        self.desc_label.config(text="Grilled chicken with lettuce, tomato & sauce")
        try:
            self.img = load_image("images/burqer.jpeg", (420, 220))
            self.image_label.config(image=self.img)
        except:
            pass
        self.size.set("Medium")
        for v, _ in self.extra_vars:
            v.set(0)
        self.notes.delete("1.0", tk.END)
        self.update_price()
    
    def update_price(self):
        total = self.base_price + self.size_prices[self.size.get()]
        total += sum(p for v, p in self.extra_vars if v.get())
        total *= self.quantity
        self.price_label.config(text=f"{total} EGP")
    
    def increase(self):
        self.quantity += 1
        self.qty_label.config(text=str(self.quantity))
        self.update_price()
    
    def decrease(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.qty_label.config(text=str(self.quantity))
            self.update_price()
    
    def add_to_cart(self):
        selected_extras = [name for (name, _), (v, _) 
                          in zip(self.extras_data, self.extra_vars) if v.get()]
        item = {
            "name": self.item_name, "price": self.base_price * self.quantity,
            "qty": self.quantity, "size": self.size.get(), "extras": selected_extras,
            "notes": self.notes.get("1.0", tk.END).strip(),
            "total_price": self.calculate_total()
        }
        self.controller.cart_items.append(item)
        messagebox.showinfo("Success", "Item added to cart!")
        self.controller.show_frame("CartPage")
    
    def calculate_total(self):
        total = self.base_price + self.size_prices[self.size.get()]
        total += sum(p for v, p in self.extra_vars if v.get())
        total *= self.quantity
        return total