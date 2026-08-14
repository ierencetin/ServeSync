import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AdminPanel:
    def __init__ (self,root):
        self.root = root
        self.root.title("Restoran Yönetim Paneli - Admin")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f6f7")

        self.inventory = {}
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg= "#2c3e50", height= 80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text= "Yönetici Paneli", font= ("Helvetica", 18, "bold"), fg = "white", bg="#2c3e50").pack(pady= 25, padx= 15)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.stok_tab = tk.Frame(self.notebook, bg= "white")
        self.notebook.add(self.stok_tab, text="📦 Stok Yönetimi")

        self.recete_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.recete_tab, text= "📋 Reçete Yönetimi")

        self.build_stok_tab()

    def build_stok_tab(self):
        form_frame = tk.Frame(self.stok_tab, bg= "#ecf0f1", width=300)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        form_frame.pack_propagate(False)

        tk.Label(form_frame, text = "Yeni Hammadde Ekle", font=("Helvetica", 14, "bold"), bg="#ecf0f1").pack(pady=15)

        #veri giriş kutuları
        tk.Label(form_frame, text="Hammadde Adı (Örn: Köfte):", bg="#ecf0f1").pack(anchor="w", padx=20, pady=5)
        self.isim_entry = ttk.Entry(form_frame, width=30)
        self.isim_entry.pack(padx=20)

        tk.Label(form_frame, text="Başlangıç Miktarı (Örn: 50):", bg="#ecf0f1").pack(anchor="w", padx=20, pady=(15, 5))
        self.miktar_entry = ttk.Entry(form_frame, width=30)
        self.miktar_entry.pack(padx=20)
        #kaydet butonu
        tk.Button(form_frame, text="Sisteme Kaydet", bg="#2980b9", fg="white", font=("Helvetica", 10, "bold"),
                  command=self.kaydet_hammadde).pack(pady=30, fill="x", padx=20)

        table_frame = tk.Frame(self.stok_tab, bg="white")
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.stok_tree = ttk.Treeview(table_frame, columns=("Madde", "Miktar"), show="headings", height=15)
        self.stok_tree.heading("Madde", text="Hammadde Adı")
        self.stok_tree.heading("Miktar", text="Miktar (Adet/Gr)")
        self.stok_tree.column("Madde", width=250)
        self.stok_tree.column("Miktar", width=150, anchor="center")
        self.stok_tree.pack(fill="both", expand=True)

    def kaydet_hammadde(self):
        isim = self.isim_entry.get().strip()
        miktar = int(self.miktar_entry.get().strip())

        if not isim or not miktar:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        if isim in self.inventory:
            self.inventory[isim] += miktar
            for row in self.stok_tree.get_children():
                if self.stok_tree.item(row, "values")[0] == isim:
                    self.stok_tree.item(row, values=(isim, self.inventory[isim]))
                    break

            messagebox.showinfo("Güncellendi",
                                f"'{isim}' stoğuna {miktar} adet eklendi. Yeni toplam: {self.inventory[isim]}")

        else:
            self.inventory[isim] = miktar
            self.stok_tree.insert("", "end", values=(isim, miktar))
            messagebox.showinfo("Başarılı", f"'{isim}' sisteme ilk kez eklendi!")

        self.isim_entry.delete(0, tk.END)
        self.miktar_entry.delete(0, tk.END)

    def yeni_urun_kaydet(self):
        isim = self.yeni_urun_isim_entry.get().title()
        fiyat = float(self.yeni_urun_fiyat_entry.get())

        secilen_recete = [
            {"hammadde_id": 1, "miktar": 1},
            {"hammadde_id": 2, "miktar": 200}
        ]

        basarili_mi, mesaj = self.db.urun_ve_recete_ekle(isim, fiyat, secilen_recete)

        if basarili_mi:
            messagebox.showinfo("Başarılı", mesaj)
        else:
            messagebox.showerror("Hata", mesaj)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()

