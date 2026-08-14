import tkinter as tk
from itertools import product
from multiprocessing import connection
from tkinter import ttk
from tkinter import messagebox
from DatabaseManager import DatabaseManager


class RestaurantPOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Lüks Restoran POS Sistemi - Masa 3")
        self.root.geometry("1024x768")
        self.root.configure(bg="#ecf0f1")

        #ürünleri tutan geçici liste
        self.current_order = []

        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        #kutu oluşturuyoruz
        self.left_frame = tk.Frame(self.root, bg="white", width = 650)
        #kutuyu nereye nasıl ve büyüdüğünde ne kadar büyüyeceğini ayarlıyoruz
        self.left_frame.pack(side = "left", fill = "both", expand = True, padx= 10, pady= 10)
        #.pack kullanmamızın sebebi ekranda görünmesini istememiz kullanmazsak arkada oluşur

        #etiket oluşturuyoruz(ne yazıcak, hangi fontta olucak vs.)
        #not : bg demek arka plan rengi demektir
        tk.Label(self.left_frame, text = "Ana yemekler", font=("Helvetica", 18, "bold"), bg = "white").pack(pady=15)

        #şimdi butonlarımızı oluşturuyoruz
        self.menu_grid = tk.Frame(self.left_frame, bg = "white")
        self.menu_grid.pack(fill = "both", expand = True, padx = 20)

        #şimdilik statik ürünler (ileride veritabanından gelecek)
        products = [
            ("Beef Wellington", 850),
            ("Kuşkonmazlı Risotto", 450),
            ("Trüf Mantarlı Makarna", 550),
            ("Chateau Petrus Kadeh", 1200)
        ]

        db_urunleri = self.db.urunleri_getir()

        #ürün butonlarını loop ile oluşturmamız gerekiyor
        for i, (name, price) in enumerate(products):
            button = tk.Button(
                self.menu_grid,
                text= f"{name} \n {price} TL",
                font= ("Helvetica", 12, "bold"),
                bg= "#3498db", fg= "white",
                height= 4, width= 20,
                command= lambda n = name, p = price: self.add_to_cart(n, p)
            )
            row = i // 2
            col = i % 2
            button.grid(row = row, column = col, padx = 15, pady = 15)

        self.right_frame = tk.Frame(self.root, bg="#2c3e50", width= 350)
        self.right_frame.pack(side = "right", fill= "both", expand= True, padx= 10, pady = 10)

        #sağ panelin boyutunu sabitledik
        self.right_frame.pack_propagate(False)

        tk.Label(self.right_frame, text = "Masa 3 - Adisyon", font=("Helvetica", 16, "bold"), fg = "white", bg = "#2c3e50").pack(pady= 15)

        #siparişlerin listelendiği tablo
        self.order_tree = ttk.Treeview(self.right_frame, columns=("Urun", "Fiyat"), show= "headings", height= 15)
        #ürünü bulup yanına text içinde yazılanı yazar
        self.order_tree.heading("Urun", text= "Ürün")
        #ürünün fiyatını bulup yanına text içinde yazılanı yazar
        self.order_tree.heading("Fiyat", text= "Fiyat (TL)")
        #ürün için yazılan text in boyutu
        self.order_tree.column("Urun", width= 180)
        #fiyat için yazılan text in boyutu
        self.order_tree.column("Fiyat", width= 80, anchor= "e")
        self.order_tree.pack(fill= "both", expand= True, padx= 15, pady= 10)

        #toplam tutar etiketi oluşturduk
        self.total_label = tk.Label(self.right_frame, text= "Toplam 0 TL", font=("Helvetica", 16, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.total_label.pack(pady=10)

        tk.Button(
            self.right_frame,
            text= "Siparişi Mutfağa Gönder",
            font= ("Helvetica", 14, "bold"),
            bg= "#27ae60",
            fg= "white",
            height= 2,
            command= self.submit_order
        ).pack(fill= "x", side= "bottom", padx= 15, pady= 20)

    #sepete ürün ekleme
    def add_to_cart(self, name, price):
        self.current_order.append({"name" : name, "price" : price})
        self.update_cart_display()

    #arayüzümüzün "tazeleme"(F5) tuşudur
    def update_cart_display(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        total_price = 0
        for item in self.current_order:
            self.order_tree.insert("", "end", values = (item["name"], f"{item['price']} TL"))
            total_price += item["price"]

        self.total_label.config(text=f"Toplam: {total_price} TL")

    def submit_order(self):
        if not self.current_order:
            messagebox.showwarning("Uyarı", "Sipariş listesi boş!")
            return

            #veritabanı sınıfımızdaki yeni yazdığımız fonksiyonu çağırıyoruz
        basarili_mi, mesaj = self.db.siparis_onayla_ve_stok_dus(self.current_order)

        if basarili_mi:
            #işlem tamamsa yeşil tikli başarı mesajı göster
            messagebox.showinfo("Başarılı", mesaj)
            #sepeti temizle ve tabloyu sıfırla
            self.current_order.clear()
            self.update_cart_display()
        else:
            #stok yetersizse veya hata varsa kırmızı çarpılı hata mesajı göster
            messagebox.showerror("Hata", mesaj)
            #sepeti temizlemiyoruz ki garson eksik ürünü silip devam edebilsin!

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantPOS(root)
    root.mainloop()
