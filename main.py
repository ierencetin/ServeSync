import tkinter as tk
# Dosyalar aynı klasörde olduğu için doğrudan dosya adından sınıfı çağırıyoruz:
# from dosya_adi import SinifAdi
from DatabaseManager import DatabaseManager
from RestaurantPOS import RestaurantPOS

def ana_uygulamayi_baslat():
    # 1. Veritabanını başlat
    db = DatabaseManager()

    # 2. Arayüzü başlat ve veritabanını arayüze bağla
    root = tk.Tk()
    app = RestaurantPOS(root, db)

    # 3. Döngüyü çalıştır
    root.mainloop()

if __name__ == "__main__":
    ana_uygulamayi_baslat()