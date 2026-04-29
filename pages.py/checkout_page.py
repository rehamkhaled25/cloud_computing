import tkinter as tk
from tkinter import messagebox
from config import COLORS

class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Back button
        tk.Button(self, text="← Back", bg="#FCC900", fg="white", bd=0,
                 padx=15, pady=5, command=self.go_back).pack(anchor="w", padx=20, pady=10)
        
        # Title
        tk.Label(self, text="Checkout", font=("Arial", 24), bg="#f2f2f2"
                ).pack(pady=(0, 20))
        
        # White card
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Total (will be updated from cart)
        self.total_label = tk.Label(card, text="Total: 0 EGP", font=("Arial", 20, "bold"),
                                    fg="#FCC900", bg="white")
        self.total_label.pack(pady=(0, 20))
        
        # Address
        tk.Label(card, text="Address:", font=("Arial", 12), bg="white", anchor="w"
                ).pack(fill="x")
        self.address = tk.Entry(card, font=("Arial", 11), bd=1, relief="solid")
        self.address.pack(fill="x", pady=(0, 15))
        self.address.insert(0, "Enter delivery address")
        
        # Phone
        tk.Label(card, text="Phone:", font=("Arial", 12), bg="white", anchor="w"
                ).pack(fill="x")
        self.phone = tk.Entry(card, font=("Arial", 11), bd=1, relief="solid")
        self.phone.pack(fill="x", pady=(0, 15))
        self.phone.insert(0, "Phone number")
        
        # Payment method
        tk.Label(card, text="Payment:", font=("Arial", 12), bg="white", anchor="w"
                ).pack(fill="x")
        
        payment_frame = tk.Frame(card, bg="white")
        payment_frame.pack(fill="x", pady=(5, 20))
        
        self.payment = tk.StringVar(value="Cash")
        tk.Radiobutton(payment_frame, text="Cash on Delivery", variable=self.payment,
                      value="Cash", bg="white", font=("Arial", 11)).pack(side="left", padx=(0, 20))
        tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment,
                      value="Card", bg="white", font=("Arial", 11)).pack(side="left")
        
        # Confirm button
        tk.Button(card, text="Confirm Order", bg="#FCC900", fg="white",
                 font=("Arial", 14), bd=0, pady=10, command=self.finish
                 ).pack(fill="x")
    
    def go_back(self):
        self.controller.show_frame("CartPage")
    
    def refresh_total(self):
        """Call this before showing the page to get total from cart"""
        total = sum(item.get('total_price', item.get('price', 0)) 
                   for item in self.controller.cart_items)
        self.total_label.config(text=f"Total: {total} EGP")
        return total
    
    def finish(self):
        addr = self.address.get().strip()
        phone = self.phone.get().strip()
        total = self.refresh_total()
        
        if addr == "Enter delivery address" or len(addr) < 5:
            messagebox.showerror("Error", "Enter valid address")
        elif phone == "Phone number" or len(phone) < 8:
            messagebox.showerror("Error", "Enter valid phone number")
        elif not self.controller.cart_items:
            messagebox.showerror("Error", "Cart is empty")
        else:
            messagebox.showinfo("Success", f"Order confirmed!\nTotal: {total} EGP\nPayment: {self.payment.get()}")
            self.controller.cart_items = []
            self.controller.show_frame("RestaurantPage")