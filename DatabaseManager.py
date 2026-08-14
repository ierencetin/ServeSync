import mysql.connector

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="restoran_db"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("MySQL Bağlantısı Başarıyla Kuruldu!")

        except mysql.connector.Error as err:
            print(f"Veritabanı Bağlantı Hatası: {err}")

    def stoklari_getir(self):
        """Hammaddeler tablosundaki tüm güncel stokları çeker."""
        sorgu = "SELECT * FROM Hammaddeler"
        self.cursor.execute(sorgu)
        return self.cursor.fetchall()

    def siparis_onayla_ve_stok_dus(self, siparis_listesi):
        try:
            self.conn.start_transaction()
            for item in siparis_listesi:
                urun_adi = item["name"]
                sorgu_urun = "SELECT urun_id FROM Urunler WHERE isim = %s"
                self.cursor.execute(sorgu_urun, (urun_adi,))
                urun = self.cursor.fetchone()

                if not urun:
                    continue  # Ürün menüde yoksa diğerine geç

                urun_id = urun["urun_id"]

                sorgu_recete = "SELECT hammadde_id, kullanilan_miktar FROM Receteler WHERE urun_id = %s"
                self.cursor.execute(sorgu_recete, (urun_id,))
                recete_icerigi = self.cursor.fetchall()

                for malzeme in recete_icerigi:
                    h_id = malzeme["hammadde_id"]
                    harcanacak = malzeme["kullanilan_miktar"]

                    sorgu_kontrol = "SELECT isim, miktar FROM Hammaddeler WHERE hammadde_id = %s"
                    self.cursor.execute(sorgu_kontrol, (h_id,))
                    stok_bilgisi = self.cursor.fetchone()

                    mevcut_stok = stok_bilgisi["miktar"]
                    hammadde_ismi = stok_bilgisi["isim"]

                    if mevcut_stok < harcanacak:
                        self.conn.rollback()
                        hata_mesaji = f"Sipariş İptal Edildi!\n\nYetersiz stok: '{hammadde_ismi}'\nGereken: {harcanacak} | Depodaki: {mevcut_stok}"
                        return False, hata_mesaji

                    sorgu_guncelle = "UPDATE Hammaddeler SET miktar = miktar - %s WHERE hammadde_id = %s"
                    self.cursor.execute(sorgu_guncelle, (harcanacak, h_id))

            self.conn.commit()
            return True, "Sipariş başarıyla mutfağa iletildi ve stoklar güncellendi."

        except mysql.connector.Error as err:
            self.conn.rollback()
            return False, f"Veritabanı Hatası: {err}"

    def urunleri_getir(self):
        """Menüde gösterilecek ürünleri Urunler tablosundan çeker."""
        try:
            sorgu = "SELECT isim, fiyat FROM Urunler"
            self.cursor.execute(sorgu)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Ürünleri çekerken hata oluştu: {err}")
            return []

    def urun_ve_recete_ekle(self, urun_adi, fiyat, recete_listesi):
        """
        Yeni ürünü ve reçetesini veritabanına kaydeder.
        recete_listesi formatı: [{"hammadde_id": 1, "miktar": 2}, {"hammadde_id": 2, "miktar": 200}]
        """
        try:
            self.conn.start_transaction()

            sorgu_urun = "INSERT INTO Urunler (isim, fiyat) VALUES (%s, %s)"
            self.cursor.execute(sorgu_urun, (urun_adi, fiyat))

            yeni_urun_id = self.cursor.lastrowid

            sorgu_recete = """
                INSERT INTO Receteler (urun_id, hammadde_id, kullanilan_miktar) 
                VALUES (%s, %s, %s)
            """

            for malzeme in recete_listesi:
                h_id = malzeme["hammadde_id"]
                miktar = malzeme["miktar"]

                self.cursor.execute(sorgu_recete, (yeni_urun_id, h_id, miktar))

            self.conn.commit()
            return True, f"'{urun_adi}' menüye başarıyla eklendi!"

        except mysql.connector.Error as err:
            self.conn.rollback()
            return False, f"Veritabanı Hatası: {err}"


