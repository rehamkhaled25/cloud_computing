import tkinter as tk
from config import COLORS

class CartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_light"])
        self.controller = controller
        tk.Label(self, text="Your Basket", font=("Arial", 22), bg=COLORS["primary"], pady=20).pack(fill="x")
        self.list_frame = tk.Frame(self, bg=COLORS["bg_light"])
        self.list_frame.pack(fill="both", expand=True, padx=50)
        
        self.total_val = tk.Label(self, text="", font=("Arial", 18), fg="#FCC900", bg=COLORS["bg_light"])
        self.total_val.pack()

        tk.Button(self, text="Checkout", bg="black", fg=COLORS["primary"], font=("Arial", 14),
                  pady=15, command=lambda: controller.show_frame("CheckoutPage")).pack(fill="x", padx=50, pady=20)

    def refresh_cart(self):
        for w in self.list_frame.winfo_children(): 
            w.destroy()
        
      
        total = sum(item.get('total_price', item.get('price', 0)) for item in self.controller.cart_items)
        
        for item in self.controller.cart_items:
            f = tk.Frame(self.list_frame, bg="white", pady=10)
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"{item['qty']}x {item['name']}", bg="white").pack(side="left", padx=10)
            
          
            item_total = item.get('total_price', item.get('price', 0))
            tk.Label(f, text=f"{item_total} EGP", bg="white", font=("Arial", 10)).pack(side="right", padx=10)
        
        self.total_val.config(text=f"Grand Total: {total} EGP")
