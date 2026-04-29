import tkinter as tk
from config import COLORS
from pages import RestaurantPage, MenuPage, ItemDetailsPage, CartPage, CheckoutPage

class GoEatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GoEats")
        self.geometry("1100x750")
        self.configure(bg=COLORS["bg_light"])

        self.cart_items = [] 

        self.container = tk.Frame(self, bg=COLORS["bg_light"])
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (RestaurantPage, MenuPage, ItemDetailsPage, CartPage, CheckoutPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RestaurantPage")

    def show_frame(self, page_name):
        if page_name == "CartPage":
            self.frames["CartPage"].refresh_cart()
        elif page_name == "CheckoutPage":
            self.frames["CheckoutPage"].refresh_total()  
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    GoEatsApp().mainloop()
