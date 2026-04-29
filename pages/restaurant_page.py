import tkinter as tk
from PIL import Image, ImageTk

class RestaurantPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f7f7f7")
        self.controller = controller
        self.images = []  

       
        self.restaurants = [
            ("images/sushi.png", "Jo Sushi", "Sushi"),
            ("images/lebanon.jpeg", "Taboon", "Lebanese"),
            ("images/delivery.jpeg", "Abou Ramy", "Sandwiches"),
            ("images/masri.jpg", "Dawar Farah", "Egyptian"),
            ("images/acai.jpg", "Quality", "Acai"),
            ("images/african.jpg", "Planet Africa", "International"),
            ("images/indian.jpg", "Indira", "Indian"),
            ("images/asian.jpeg", "Lan Yuan", "Asian"),
            ("images/rill.png", "Elsawy", "Pizza & Grills"),
            ("images/hadramot.jpeg", "Hadrmout", "Mandi"),
            ("images/burger.jpg", "Burger King", "Burgers"),
            ("images/kfc.jpg", "KFC", "Fried Chicken"),
            ("images/starbucks.jpg", "Starbucks", "Coffee"),
            ("images/mcdonalds.jpg", "McDonald's", "Burgers"),
            ("images/pizza.jpg", "Pizza Hut", "Pizza"),
        ]

        
        tk.Label(self, text="GoEats", bg="#f7f7f7", fg="#FCC900", 
                font=("Arial", 36, "bold")).pack(pady=(10, 0))
        tk.Label(self, text="Fast delivery of food, groceries and more",
                bg="#f7f7f7", fg="#666", font=("Arial", 12)).pack(pady=(0, 10))

       
        search_frame = tk.Frame(self, bg="white", bd=1)
        search_frame.pack(pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_restaurants)
        
        tk.Entry(search_frame, textvariable=self.search_var, width=50, 
                font=("Arial", 11), bd=0).pack(side="left", padx=10, pady=5)
        tk.Button(search_frame, text="Search", bg="#FCC900", fg="white",
                 font=("Arial", 10, "bold"), bd=0, padx=15, pady=5,
                 command=self.filter_restaurants).pack(side="left", padx=(0, 5))

     
        tk.Label(self, text="All Restaurants", bg="#eaeaea", 
                font=("Arial", 12), pady=5).pack(fill="x", pady=(10, 8))

       
        center_container = tk.Frame(self, bg="#f7f7f7")
        center_container.pack(expand=True, fill="both")
        
        
        self.grid_frame = tk.Frame(center_container, bg="#f7f7f7")
        self.grid_frame.pack(expand=True)

       
        for c in range(5):
            self.grid_frame.grid_columnconfigure(c)

        
        self.filter_restaurants()

       
        footer = tk.Frame(self, bg="#f0f0f0")
        footer.pack(fill="x", side="bottom")
        tk.Frame(footer, height=1).pack(fill="x")
        tk.Label(footer, text="© 2026 GoEats | Delivering happiness to your door",
                bg="#f0f0f0", fg="#666", font=("Arial", 8)).pack(pady=8)

    def load_local_image(self, path, size=None):
        try:
            im = Image.open(path)
            if size:
                im = im.resize(size)
            return ImageTk.PhotoImage(im)
        except:
            return None

    def filter_restaurants(self, *args):
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.images = []
        
        query = self.search_var.get().lower()
        filtered = [r for r in self.restaurants if query in r[1].lower() or query in r[2].lower()]

        # Display in 5 columns - CENTERED
        for i, (path, name, cat) in enumerate(filtered):
            row = i // 5
            col = i % 5

            card = tk.Frame(self.grid_frame, bg="white", relief="solid", bd=1)
            card.grid(row=row, column=col, padx=10, pady=8)

            img = self.load_local_image(path, (130, 85))
            if img:
                self.images.append(img)
                tk.Label(card, image=img, bg="white").pack(pady=(8, 2))
            else:
                # Placeholder for missing images
                tk.Label(card, text="🍽️", bg="#eee", font=("Arial", 30), 
                        width=5, height=1).pack(pady=(8, 2))

            tk.Label(card, text=name, bg="white", font=("Arial", 9)).pack()
            tk.Label(card, text=cat, bg="white", fg="#666", font=("Arial", 8)).pack()
            
            tk.Button(card, text="View Menu", bg="#FCC900", fg="white",
                     font=("Arial", 8, "bold"), bd=0, padx=10, pady=3,
                     command=lambda: self.controller.show_frame("MenuPage")).pack(pady=(5, 8))