import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import os
import hashlib
import csv
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Veri dosyası
DATA_FILE = "crm_data.json"

kullanicilar = []
musteriler = []
satislar = []
destek_talepleri = []

class Veritabani:
    @staticmethod
    def veri_kaydet():
        """Tüm verileri JSON dosyasına kaydeder."""
        veri = {
            'kullanicilar': kullanicilar,
            'musteriler': musteriler,
            'satislar': satislar,
            'destek_talepleri': destek_talepleri
        }
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as dosya:
                json.dump(veri, dosya, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Veri kaydedilirken hata: {e}")

    @staticmethod
    def veri_yukle():
        """JSON dosyasından verileri yükler."""
        global kullanicilar, musteriler, satislar, destek_talepleri
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as dosya:
                    veri = json.load(dosya)
                    kullanicilar = veri.get('kullanicilar', [])
                    musteriler = veri.get('musteriler', [])
                    satislar = veri.get('satislar', [])
                    destek_talepleri = veri.get('destek_talepleri', [])
            except Exception as e:
                print(f"Veri yüklenirken hata: {e}")
                kullanicilar = []
                musteriler = []
                satislar = []
                destek_talepleri = []
        else:
            # İlk kullanım için varsayılan admin kullanıcısı ekle
            Kullanici.kullanici_ekle("admin", "12345", {
                'musteri_yonetimi': True,
                'satis_yonetimi': True,
                'destek_yonetimi': True
            })

    @staticmethod
    def sifrele(metin):
        return hashlib.sha256(metin.encode()).hexdigest()

class Kullanici:
    @staticmethod
    def kullanici_ekle(kullanici_adi, sifre, yetkiler=None):
        for kullanici in kullanicilar:
            if kullanici['kullanici_adi'] == kullanici_adi:
                return False
        if not yetkiler:
            yetkiler = {
                'musteri_yonetimi': True,
                'satis_yonetimi': True,
                'destek_yonetimi': True
            }
        kullanicilar.append({
            'id': len(kullanicilar) + 1,
            'kullanici_adi': kullanici_adi,
            'sifre': Veritabani.sifrele(sifre),
            'yetkiler': yetkiler,
            'son_giris': None
        })
        Veritabani.veri_kaydet()
        return True

    @staticmethod
    def kullanici_giris(kullanici_adi, sifre):
        for kullanici in kullanicilar:
            if kullanici['kullanici_adi'] == kullanici_adi and kullanici['sifre'] == Veritabani.sifrele(sifre):
                kullanici['son_giris'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Veritabani.veri_kaydet()
                return kullanici
        return None

class Musteri:
    @staticmethod
    def musteri_ekle(musteri_tipi, ad=None, soyad=None, firma_adi=None, telefon=None, eposta=None, adres=None, notlar=None, vergi_no=None):
        if musteri_tipi == 'bireysel':
            if not re.match(r'^[A-Za-z\s]{2,}$', ad) or not re.match(r'^[A-Za-z\s]{2,}$', soyad):
                return None
        elif musteri_tipi == 'kurumsal':
            if not re.match(r'^[A-Za-z0-9\s]{2,}$', firma_adi):
                return None
            if vergi_no and not re.match(r'^\d{10,11}$', vergi_no):
                return None
        else:
            return None

        if telefon and not re.match(r'^\+?\d{10,15}$', telefon):
            return None
        if eposta and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', eposta):
            return None

        for musteri in musteriler:
            if musteri_tipi == 'bireysel' and musteri['musteri_tipi'] == 'bireysel':
                if musteri['ad'] == ad and musteri['soyad'] == soyad:
                    return None
            elif musteri_tipi == 'kurumsal' and musteri['musteri_tipi'] == 'kurumsal':
                if musteri['firma_adi'] == firma_adi:
                    return None

        musteri_id = len(musteriler) + 1
        musteri = {
            'id': musteri_id,
            'musteri_tipi': musteri_tipi,
            'ad': ad if musteri_tipi == 'bireysel' else None,
            'soyad': soyad if musteri_tipi == 'bireysel' else None,
            'firma_adi': firma_adi if musteri_tipi == 'kurumsal' else None,
            'telefon': telefon,
            'eposta': eposta,
            'adres': adres,
            'notlar': notlar,
            'vergi_no': vergi_no if musteri_tipi == 'kurumsal' else None,
            'kayit_tarihi': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        musteriler.append(musteri)
        Veritabani.veri_kaydet()
        return musteri_id

    @staticmethod
    def musteri_duzenle(musteri_id, **kwargs):
        for musteri in musteriler:
            if musteri['id'] == musteri_id:
                musteri_tipi = musteri['musteri_tipi']
                if musteri_tipi == 'bireysel':
                    if 'ad' in kwargs and not re.match(r'^[A-Za-z\s]{2,}$', kwargs['ad']):
                        return False
                    if 'soyad' in kwargs and not re.match(r'^[A-Za-z\s]{2,}$', kwargs['soyad']):
                        return False
                elif musteri_tipi == 'kurumsal':
                    if 'firma_adi' in kwargs and not re.match(r'^[A-Za-z0-9\s]{2,}$', kwargs['firma_adi']):
                        return False
                    if 'vergi_no' in kwargs and kwargs['vergi_no'] and not re.match(r'^\d{10,11}$', kwargs['vergi_no']):
                        return False
                if 'telefon' in kwargs and kwargs['telefon'] and not re.match(r'^\+?\d{10,15}$', kwargs['telefon']):
                    return False
                if 'eposta' in kwargs and kwargs['eposta'] and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', kwargs['eposta']):
                    return False
                for key, value in kwargs.items():
                    musteri[key] = value
                Veritabani.veri_kaydet()
                return True
        return False

    @staticmethod
    def musteri_sil(musteri_id):
        global musteriler
        musteri = Musteri.musteri_getir(musteri_id)
        if musteri:
            musteriler = [m for m in musteriler if m['id'] != musteri_id]
            Veritabani.veri_kaydet()
            return True
        return False

    @staticmethod
    def musteri_getir(musteri_id):
        for musteri in musteriler:
            if musteri['id'] == musteri_id:
                return musteri
        return None

    @staticmethod
    def musterileri_listele(filtre=None):
        if filtre:
            return [m for m in musteriler if filtre.lower() in (
                f"{m['ad']} {m['soyad']}".lower() if m['musteri_tipi'] == 'bireysel' else m['firma_adi'].lower()
            )]
        return musteriler

    @staticmethod
    def satis_ekle(musteri_id, urunler, toplam_tutar, aciklama=None):
        satis_id = len(satislar) + 1
        satis = {
            'id': satis_id,
            'musteri_id': musteri_id,
            'urunler': urunler,
            'toplam_tutar': toplam_tutar,
            'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'aciklama': aciklama
        }
        satislar.append(satis)
        Veritabani.veri_kaydet()
        return satis_id

    @staticmethod
    def destek_talebi_olustur(musteri_id, konu, detay, durum='açık'):
        talep_id = len(destek_talepleri) + 1
        talep = {
            'id': talep_id,
            'musteri_id': musteri_id,
            'konu': konu,
            'detay': detay,
            'durum': durum,
            'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'guncelleme_tarihi': None
        }
        destek_talepleri.append(talep)
        Veritabani.veri_kaydet()
        return talep_id

class Satis:
    @staticmethod
    def satis_getir(satis_id):
        for satis in satislar:
            if satis['id'] == satis_id:
                return satis
        return None

    @staticmethod
    def satis_listele(musteri_id=None, baslangic_tarihi=None, bitis_tarihi=None):
        result = []
        for s in satislar:
            if musteri_id and s['musteri_id'] != musteri_id:
                continue
            if baslangic_tarihi and bitis_tarihi:
                if not (baslangic_tarihi <= s['tarih'][:10] <= bitis_tarihi):
                    continue
            result.append(s)
        return result

class Destek:
    @staticmethod
    def talep_getir(talep_id):
        for talep in destek_talepleri:
            if talep['id'] == talep_id:
                return talep
        return None

    @staticmethod
    def talep_listele(musteri_id=None):
        if musteri_id:
            return [t for t in destek_talepleri if t['musteri_id'] == musteri_id]
        return destek_talepleri

    @staticmethod
    def talep_durum_guncelle(talep_id, durum):
        for talep in destek_talepleri:
            if talep['id'] == talep_id:
                talep['durum'] = durum
                talep['guncelleme_tarihi'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Veritabani.veri_kaydet()
                return True
        return False

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        style = ttk.Style()
        style.configure('Modern.TButton',
                        font=('Helvetica', 10, 'bold'),
                        padding=10,
                        foreground='#ffffff',
                        background='#3B82F6',
                        bordercolor='#3B82F6',
                        lightcolor='#3B82F6',
                        darkcolor='#2563EB')
        style.map('Modern.TButton',
                  background=[('active', '#2563EB')],
                  foreground=[('active', '#ffffff')])
        kwargs['style'] = 'Modern.TButton'
        super().__init__(master, **kwargs)

class CRMUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş CRM Sistemi")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        self.kullanici = None
        self.yetkiler = {}
        self.tema = 'açık'
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=30, font=('Helvetica', 11))
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'))
        self.style.configure('Card.TFrame', background='#ffffff', borderwidth=1, relief='flat')
        Veritabani.veri_yukle()
        self.otomatik_yedek_baslat()
        self.giris_ekrani()

    def otomatik_yedek_baslat(self):
        def yedekle():
            while True:
                Veritabani.veri_kaydet()
                time.sleep(600)  # 10 dakikada bir
        threading.Thread(target=yedekle, daemon=True).start()

    def tema_degistir(self):
        if self.tema == 'açık':
            self.tema = 'koyu'
            self.root.configure(bg='#1F2937')
            self.style.configure('Card.TFrame', background='#374151')
            self.style.configure('Treeview', background='#374151', fieldbackground='#374151', foreground='#ffffff')
            self.style.configure('Treeview.Heading', background='#4B5563', foreground='#ffffff')
        else:
            self.tema = 'açık'
            self.root.configure(bg='#F3F4F6')
            self.style.configure('Card.TFrame', background='#ffffff')
            self.style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#000000')
            self.style.configure('Treeview.Heading', background='#e0e0e0', foreground='#000000')
        self.ana_ekran()

    def giris_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#F3F4F6')
        
        login_frame = ttk.Frame(self.root, style='Card.TFrame')
        login_frame.place(relx=0.5, rely=0.5, anchor='center', width=400)
        
        ttk.Label(login_frame,
                  text="CRM Sistemi",
                  font=('Helvetica', 20, 'bold'),
                  background='#ffffff').grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(login_frame,
                  text="Kullanıcı Adı:",
                  font=('Helvetica', 11),
                  background='#ffffff').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.kullanici_adi_entry = ttk.Entry(login_frame, font=('Helvetica', 11))
        self.kullanici_adi_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(login_frame,
                  text="Şifre:",
                  font=('Helvetica', 11),
                  background='#ffffff').grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.sifre_entry = ttk.Entry(login_frame, show="*", font=('Helvetica', 11))
        self.sifre_entry.grid(row=2, column=1, padx=10, pady=5)
        
        giris_btn = ModernButton(login_frame, text="Giriş Yap",
                               command=self.giris_yap)
        giris_btn.grid(row=3, column=0, columnspan=2, pady=15, ipadx=20)
        
        kayit_btn = ttk.Button(login_frame, text="Yeni Kullanıcı Kaydı",
                              command=self.kullanici_kayit_ekrani)
        kayit_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.root.bind('<Return>', lambda event: self.giris_yap())
        self.kullanici_adi_entry.focus()

    def kullanici_kayit_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Kullanıcı Kaydı")
        pencere.geometry("400x400")
        
        form_frame = ttk.Frame(pencere)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Kullanıcı Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        k_adi_entry = ttk.Entry(form_frame)
        k_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Şifre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        sifre_entry = ttk.Entry(form_frame, show="*")
        sifre_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Şifre Tekrar:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sifre_tekrar_entry = ttk.Entry(form_frame, show="*")
        sifre_tekrar_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Yetkiler:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        musteri_yonetimi = tk.BooleanVar(value=True)
        satis_yonetimi = tk.BooleanVar(value=True)
        destek_yonetimi = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Müşteri Yönetimi", variable=musteri_yonetimi).grid(row=3, column=1, sticky='w')
        ttk.Checkbutton(form_frame, text="Satış Yönetimi", variable=satis_yonetimi).grid(row=4, column=1, sticky='w')
        ttk.Checkbutton(form_frame, text="Destek Yönetimi", variable=destek_yonetimi).grid(row=5, column=1, sticky='w')
        
        def kaydet():
            if not k_adi_entry.get() or not sifre_entry.get():
                messagebox.showerror("Hata", "Kullanıcı adı ve şifre zorunludur")
                return
            if sifre_entry.get() != sifre_tekrar_entry.get():
                messagebox.showerror("Hata", "Şifreler uyuşmuyor")
                return
            yetkiler = {
                'musteri_yonetimi': musteri_yonetimi.get(),
                'satis_yonetimi': satis_yonetimi.get(),
                'destek_yonetimi': destek_yonetimi.get()
            }
            if Kullanici.kullanici_ekle(k_adi_entry.get(), sifre_entry.get(), yetkiler):
                messagebox.showinfo("Başarılı", "Kullanıcı kaydedildi")
                pencere.destroy()
            else:
                messagebox.showerror("Hata", "Kullanıcı adı zaten alınmış")
        
        ModernButton(form_frame, text="Kayıt Ol", command=kaydet).grid(row=6, column=0, columnspan=2, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        k_adi_entry.focus()

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi_entry.get().strip()
        sifre = self.sifre_entry.get()
        
        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre giriniz")
            return
        
        kullanici = Kullanici.kullanici_giris(kullanici_adi, sifre)
        if kullanici:
            self.kullanici = kullanici
            self.yetkiler = kullanici['yetkiler']
            self.ana_ekran()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış\nVarsayılan: admin/12345")

    def ana_ekran(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#F3F4F6' if self.tema == 'açık' else '#1F2937')
        
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        dosya_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Dosya", menu=dosya_menu)
        dosya_menu.add_command(label="Yedek Al", command=self.yedek_al)
        dosya_menu.add_command(label="Yedekten Yükle", command=self.yedekten_yukle)
        dosya_menu.add_command(label="Tema Değiştir", command=self.tema_degistir)
        dosya_menu.add_separator()
        dosya_menu.add_command(label="Çıkış", command=self.giris_ekrani)
        
        islem_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="İşlemler", menu=islem_menu)
        if self.yetkiler.get('musteri_yonetimi', False):
            islem_menu.add_command(label="Müşteri Ekle", command=self.musteri_ekle_ekrani, accelerator="Ctrl+M")
        if self.yetkiler.get('satis_yonetimi', False):
            islem_menu.add_command(label="Satış Ekle", command=self.satis_ekle_ekrani, accelerator="Ctrl+S")
        if self.yetkiler.get('destek_yonetimi', False):
            islem_menu.add_command(label="Destek Talebi Oluştur", command=self.destek_talebi_ekrani, accelerator="Ctrl+D")
        
        rapor_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Raporlar", menu=rapor_menu)
        rapor_menu.add_command(label="Satış Raporu", command=self.satis_raporu_ekrani)
        
        yardim_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Yardım", menu=yardim_menu)
        yardim_menu.add_command(label="Kullanım Kılavuzu", command=self.kullanim_kilavuzu)
        yardim_menu.add_command(label="Hakkında", command=self.hakkinda)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        sol_frame = ttk.Frame(main_frame, width=250, style='Card.TFrame')
        sol_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        sag_frame = ttk.Frame(main_frame, style='Card.TFrame')
        sag_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(sol_frame, text="Hızlı Erişim", font=('Helvetica', 14, 'bold')).pack(pady=10)
        if self.yetkiler.get('musteri_yonetimi', False):
            ModernButton(sol_frame, text="Müşteri Ekle", command=self.musteri_ekle_ekrani).pack(fill='x', pady=5, padx=5)
        if self.yetkiler.get('satis_yonetimi', False):
            ModernButton(sol_frame, text="Satış Ekle", command=self.satis_ekle_ekrani).pack(fill='x', pady=5, padx=5)
        if self.yetkiler.get('destek_yonetimi', False):
            ModernButton(sol_frame, text="Destek Talebi", command=self.destek_talebi_ekrani).pack(fill='x', pady=5, padx=5)
        ModernButton(sol_frame, text="Satış Raporu", command=self.satis_raporu_ekrani).pack(fill='x', pady=5, padx=5)
        
        ttk.Label(sol_frame, text="Son Müşteriler", font=('Helvetica', 14, 'bold')).pack(pady=10)
        for m in musteriler[-5:]:
            if m['musteri_tipi'] == 'bireysel':
                isim = f"{m['ad']} {m['soyad']}"
            else:
                isim = m['firma_adi']
            ttk.Label(sol_frame,
                      text=isim,
                      foreground='#EF4444' if self.tema == 'açık' else '#F87171').pack(anchor='w', padx=10)
        
        notebook = ttk.Notebook(sag_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        musteriler_frame = ttk.Frame(notebook)
        satislar_frame = ttk.Frame(notebook)
        destek_frame = ttk.Frame(notebook)
        
        notebook.add(musteriler_frame, text="📋 Müşteriler")
        notebook.add(satislar_frame, text="💸 Satışlar")
        notebook.add(destek_frame, text="🛠 Destek Talepleri")
        
        self.musteriler_listesi(musteriler_frame)
        self.satislar_listesi(satislar_frame)
        self.destek_talepleri_listesi(destek_frame)
        
        durum_cubugu = ttk.Label(self.root,
                                text=f"Kullanıcı: {self.kullanici['kullanici_adi']} | Son Giriş: {self.kullanici['son_giris']}",
                                relief=tk.SUNKEN,
                                anchor=tk.W)
        durum_cubugu.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.root.bind('<Control-m>', lambda event: self.musteri_ekle_ekrani() if self.yetkiler.get('musteri_yonetimi', False) else None)
        self.root.bind('<Control-s>', lambda event: self.satis_ekle_ekrani() if self.yetkiler.get('satis_yonetimi', False) else None)
        self.root.bind('<Control-d>', lambda event: self.destek_talebi_ekrani() if self.yetkiler.get('destek_yonetimi', False) else None)

    def musteriler_listesi(self, parent):
        arama_frame = ttk.Frame(parent, style='Card.TFrame')
        arama_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(arama_frame, text="Ara:").pack(side=tk.LEFT, padx=5)
        arama_entry = ttk.Combobox(arama_frame,
                                  values=[f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi'] for m in Musteri.musterileri_listele()])
        arama_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        columns = ("ID", "Tip", "İsim/Firma", "Telefon", "E-posta", "Adres", "Kayıt Tarihi")
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column("İsim/Firma", width=150, anchor='w')
        tree.column("Adres", width=200, anchor='w')
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def guncelle_liste(event=None):
            for item in tree.get_children():
                tree.delete(item)
            filtre = arama_entry.get()
            musteri_listesi = Musteri.musterileri_listele(filtre)
            for m in musteri_listesi:
                isim = f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi']
                tree.insert('', tk.END,
                           values=(m['id'], m['musteri_tipi'], isim,
                                   m['telefon'] or '', m['eposta'] or '',
                                   m['adres'] or '', m['kayit_tarihi']))
        
        tree_menu = tk.Menu(self.root, tearoff=0)
        if self.yetkiler.get('musteri_yonetimi', False):
            tree_menu.add_command(label="Düzenle", command=lambda: self.musteri_duzenle(tree))
            tree_menu.add_command(label="Sil", command=lambda: self.musteri_sil(tree))
        tree_menu.add_command(label="Satışları Görüntüle", command=lambda: self.musteri_satislar(tree))
        tree_menu.add_command(label="Destek Talepleri", command=lambda: self.musteri_destek_talepleri(tree))
        
        def sag_tik(event):
            try:
                tree.selection_set(tree.identify_row(event.y))
                tree_menu.post(event.x_root, event.y_root)
            except:
                pass
        
        tree.bind("<Button-3>", sag_tik)
        arama_entry.bind('<KeyRelease>', guncelle_liste)
        arama_entry.bind('<Return>', guncelle_liste)
        guncelle_liste()

    def satislar_listesi(self, parent):
        arama_frame = ttk.Frame(parent, style='Card.TFrame')
        arama_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(arama_frame, text="Ara (Müşteri Adı):").pack(side=tk.LEFT, padx=5)
        arama_entry = ttk.Combobox(arama_frame,
                                  values=[f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi'] for m in Musteri.musterileri_listele()])
        arama_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        columns = ("ID", "Müşteri", "Ürünler", "Toplam Tutar", "Tarih", "Açıklama")
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column("Müşteri", width=150, anchor='w')
        tree.column("Ürünler", width=200, anchor='w')
        tree.column("Açıklama", width=200, anchor='w')
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def guncelle_liste(event=None):
            for item in tree.get_children():
                tree.delete(item)
            filtre = arama_entry.get()
            satis_listesi = Satis.satis_listele()
            for s in satis_listesi:
                musteri = Musteri.musteri_getir(s['musteri_id'])
                if musteri:
                    musteri_adi = f"{musteri['ad']} {musteri['soyad']}" if musteri['musteri_tipi'] == 'bireysel' else musteri['firma_adi']
                    if not filtre or filtre.lower() in musteri_adi.lower():
                        urunler_str = ", ".join([u['ad'] for u in s['urunler']])
                        tree.insert('', tk.END,
                                   values=(s['id'], musteri_adi,
                                           urunler_str, f"{s['toplam_tutar']:.2f}",
                                           s['tarih'], s['aciklama'] or ''))
        
        arama_entry.bind('<KeyRelease>', guncelle_liste)
        arama_entry.bind('<Return>', guncelle_liste)
        guncelle_liste()

    def destek_talepleri_listesi(self, parent):
        arama_frame = ttk.Frame(parent, style='Card.TFrame')
        arama_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(arama_frame, text="Ara (Müşteri Adı):").pack(side=tk.LEFT, padx=5)
        arama_entry = ttk.Combobox(arama_frame,
                                  values=[f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi'] for m in Musteri.musterileri_listele()])
        arama_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        columns = ("ID", "Müşteri", "Konu", "Detay", "Durum", "Tarih", "Güncelleme Tarihi")
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column("Müşteri", width=150, anchor='w')
        tree.column("Konu", width=150, anchor='w')
        tree.column("Detay", width=200, anchor='w')
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def guncelle_liste(event=None):
            for item in tree.get_children():
                tree.delete(item)
            filtre = arama_entry.get()
            talep_listesi = Destek.talep_listele()
            for t in talep_listesi:
                musteri = Musteri.musteri_getir(t['musteri_id'])
                if musteri:
                    musteri_adi = f"{musteri['ad']} {musteri['soyad']}" if musteri['musteri_tipi'] == 'bireysel' else musteri['firma_adi']
                    if not filtre or filtre.lower() in musteri_adi.lower():
                        tree.insert('', tk.END,
                                   values=(t['id'], musteri_adi,
                                           t['konu'], t['detay'], t['durum'],
                                           t['tarih'], t['guncelleme_tarihi'] or ''))
        
        tree_menu = tk.Menu(self.root, tearoff=0)
        if self.yetkiler.get('destek_yonetimi', False):
            tree_menu.add_command(label="Durum Güncelle", command=lambda: self.talep_durum_guncelle(tree))
        
        def sag_tik(event):
            try:
                tree.selection_set(tree.identify_row(event.y))
                tree_menu.post(event.x_root, event.y_root)
            except:
                pass
        
        tree.bind("<Button-3>", sag_tik)
        arama_entry.bind('<KeyRelease>', guncelle_liste)
        arama_entry.bind('<Return>', guncelle_liste)
        guncelle_liste()

    def musteri_ekle_ekrani(self):
        if not self.yetkiler.get('musteri_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Müşteri Ekle")
        pencere.geometry("450x600")
        
        form_frame = ttk.Frame(pencere, style='Card.TFrame')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Müşteri Tipi:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        musteri_tipi = ttk.Combobox(form_frame, values=['bireysel', 'kurumsal'])
        musteri_tipi.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        musteri_tipi.set('bireysel')
        
        bireysel_frame = ttk.Frame(form_frame)
        ttk.Label(bireysel_frame, text="Ad:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ad_entry = ttk.Entry(bireysel_frame)
        ad_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(bireysel_frame, text="Soyad:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        soyad_entry = ttk.Entry(bireysel_frame)
        soyad_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        kurumsal_frame = ttk.Frame(form_frame)
        ttk.Label(kurumsal_frame, text="Firma Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        firma_adi_entry = ttk.Entry(kurumsal_frame)
        firma_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(kurumsal_frame, text="Vergi No:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        vergi_no_entry = ttk.Entry(kurumsal_frame)
        vergi_no_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Telefon:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        telefon_entry = ttk.Entry(form_frame)
        telefon_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="E-posta:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        eposta_entry = ttk.Entry(form_frame)
        eposta_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Adres:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        adres_entry = ttk.Entry(form_frame)
        adres_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Notlar:").grid(row=6, column=0, padx=5, pady=5, sticky='ne')
        notlar_text = scrolledtext.ScrolledText(form_frame, height=5, wrap=tk.WORD)
        notlar_text.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        
        def guncelle_form():
            if musteri_tipi.get() == 'bireysel':
                kurumsal_frame.grid_forget()
                bireysel_frame.grid(row=1, column=0, columnspan=2, sticky='we')
            else:
                bireysel_frame.grid_forget()
                kurumsal_frame.grid(row=1, column=0, columnspan=2, sticky='we')
        
        musteri_tipi.bind('<<ComboboxSelected>>', lambda event: guncelle_form())
        guncelle_form()
        
        def kaydet():
            musteri_id = Musteri.musteri_ekle(
                musteri_tipi.get(),
                ad=ad_entry.get() if musteri_tipi.get() == 'bireysel' else None,
                soyad=soyad_entry.get() if musteri_tipi.get() == 'bireysel' else None,
                firma_adi=firma_adi_entry.get() if musteri_tipi.get() == 'kurumsal' else None,
                telefon=telefon_entry.get(),
                eposta=eposta_entry.get(),
                adres=adres_entry.get(),
                notlar=notlar_text.get("1.0", tk.END).strip(),
                vergi_no=vergi_no_entry.get() if musteri_tipi.get() == 'kurumsal' else None
            )
            if musteri_id:
                messagebox.showinfo("Başarılı", "Müşteri eklendi")
                pencere.destroy()
                self.ana_ekran()
            else:
                messagebox.showerror("Hata", "Geçersiz giriş veya müşteri zaten kayıtlı")
        
        ModernButton(form_frame, text="Kaydet", command=kaydet).grid(row=7, column=0, columnspan=2, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        musteri_tipi.focus()
        pencere.bind('<Return>', lambda event: kaydet())

    def musteri_duzenle(self, tree):
        if not self.yetkiler.get('musteri_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir müşteri seçin")
            return
        
        musteri_id = int(tree.item(selected_item)['values'][0])
        musteri = Musteri.musteri_getir(musteri_id)
        if not musteri:
            messagebox.showerror("Hata", "Müşteri bulunamadı")
            return
        
        pencere = tk.Toplevel(self.root)
        pencere.title("Müşteri Düzenle")
        pencere.geometry("450x600")
        
        form_frame = ttk.Frame(pencere, style='Card.TFrame')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Müşteri Tipi:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        musteri_tipi = ttk.Combobox(form_frame, values=['bireysel', 'kurumsal'], state='readonly')
        musteri_tipi.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        musteri_tipi.set(musteri['musteri_tipi'])
        
        bireysel_frame = ttk.Frame(form_frame)
        ttk.Label(bireysel_frame, text="Ad:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ad_entry = ttk.Entry(bireysel_frame)
        ad_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        if musteri['ad']:
            ad_entry.insert(0, musteri['ad'])
        
        ttk.Label(bireysel_frame, text="Soyad:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        soyad_entry = ttk.Entry(bireysel_frame)
        soyad_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        if musteri['soyad']:
            soyad_entry.insert(0, musteri['soyad'])
        
        kurumsal_frame = ttk.Frame(form_frame)
        ttk.Label(kurumsal_frame, text="Firma Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        firma_adi_entry = ttk.Entry(kurumsal_frame)
        firma_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        if musteri['firma_adi']:
            firma_adi_entry.insert(0, musteri['firma_adi'])
        
        ttk.Label(kurumsal_frame, text="Vergi No:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        vergi_no_entry = ttk.Entry(kurumsal_frame)
        vergi_no_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        if musteri['vergi_no']:
            vergi_no_entry.insert(0, musteri['vergi_no'])
        
        ttk.Label(form_frame, text="Telefon:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        telefon_entry = ttk.Entry(form_frame)
        telefon_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        if musteri['telefon']:
            telefon_entry.insert(0, musteri['telefon'])
        
        ttk.Label(form_frame, text="E-posta:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        eposta_entry = ttk.Entry(form_frame)
        eposta_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        if musteri['eposta']:
            eposta_entry.insert(0, musteri['eposta'])
        
        ttk.Label(form_frame, text="Adres:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        adres_entry = ttk.Entry(form_frame)
        adres_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        if musteri['adres']:
            adres_entry.insert(0, musteri['adres'])
        
        ttk.Label(form_frame, text="Notlar:").grid(row=6, column=0, padx=5, pady=5, sticky='ne')
        notlar_text = scrolledtext.ScrolledText(form_frame, height=5, wrap=tk.WORD)
        notlar_text.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        if musteri['notlar']:
            notlar_text.insert(tk.END, musteri['notlar'])
        
        def guncelle_form():
            if musteri_tipi.get() == 'bireysel':
                kurumsal_frame.grid_forget()
                bireysel_frame.grid(row=1, column=0, columnspan=2, sticky='we')
            else:
                bireysel_frame.grid_forget()
                kurumsal_frame.grid(row=1, column=0, columnspan=2, sticky='we')
        
        guncelle_form()
        
        def kaydet():
            if Musteri.musteri_duzenle(
                musteri_id,
                ad=ad_entry.get() if musteri_tipi.get() == 'bireysel' else None,
                soyad=soyad_entry.get() if musteri_tipi.get() == 'bireysel' else None,
                firma_adi=firma_adi_entry.get() if musteri_tipi.get() == 'kurumsal' else None,
                telefon=telefon_entry.get(),
                eposta=eposta_entry.get(),
                adres=adres_entry.get(),
                notlar=notlar_text.get("1.0", tk.END).strip(),
                vergi_no=vergi_no_entry.get() if musteri_tipi.get() == 'kurumsal' else None
            ):
                messagebox.showinfo("Başarılı", "Müşteri güncellendi")
                pencere.destroy()
                self.ana_ekran()
            else:
                messagebox.showerror("Hata", "Geçersiz giriş")
        
        ModernButton(form_frame, text="Kaydet", command=kaydet).grid(row=7, column=0, columnspan=2, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        musteri_tipi.focus()
        pencere.bind('<Return>', lambda event: kaydet())

    def musteri_sil(self, tree):
        if not self.yetkiler.get('musteri_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir müşteri seçin")
            return
        
        musteri_id = int(tree.item(selected_item)['values'][0])
        if messagebox.askyesno("Onay", "Müşteriyi silmek istediğinize emin misiniz?"):
            if Musteri.musteri_sil(musteri_id):
                messagebox.showinfo("Başarılı", "Müşteri silindi")
                self.ana_ekran()
            else:
                messagebox.showerror("Hata", "Müşteri silinemedi")

    def satis_ekle_ekrani(self):
        if not self.yetkiler.get('satis_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Satış Ekle")
        pencere.geometry("700x700")
        
        form_frame = ttk.Frame(pencere, style='Card.TFrame')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Müşteri:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        musteri_combobox = ttk.Combobox(form_frame,
                                       values=[f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi'] for m in Musteri.musterileri_listele()])
        musteri_combobox.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Ürünler:").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        
        urunler_frame = ttk.Frame(form_frame)
        urunler_frame.grid(row=2, column=0, columnspan=3, sticky='we')
        
        urunler_listesi = []
        columns = ("Ürün Adı", "Fiyat")
        urun_tree = ttk.Treeview(urunler_frame, columns=columns, show='headings', height=6)
        for col in columns:
            urun_tree.heading(col, text=col)
            urun_tree.column(col, width=200, anchor='w')
        urun_tree.pack(fill='x', pady=5)
        
        def urun_ekle():
            urun_ad = tk.simpledialog.askstring("Ürün Ekle", "Ürün Adı:", parent=pencere)
            if not urun_ad:
                return
            try:
                fiyat = float(tk.simpledialog.askfloat("Ürün Ekle", "Fiyat:", parent=pencere))
                if fiyat < 0:
                    raise ValueError("Fiyat negatif olamaz")
                urunler_listesi.append({'ad': urun_ad, 'fiyat': fiyat})
                urun_tree.insert('', tk.END, values=(urun_ad, f"{fiyat:.2f}"))
                toplam_guncelle()
            except (ValueError, TypeError):
                messagebox.showerror("Hata", "Geçerli bir fiyat girin")
        
        def urun_sil():
            selected = urun_tree.selection()
            if not selected:
                messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
                return
            index = urun_tree.index(selected[0])
            urun_tree.delete(selected[0])
            urunler_listesi.pop(index)
            toplam_guncelle()
        
        def toplam_guncelle():
            toplam = sum(u['fiyat'] for u in urunler_listesi)
            toplam_tutar_entry.delete(0, tk.END)
            toplam_tutar_entry.insert(0, f"{toplam:.2f}")
        
        ttk.Button(form_frame, text="Ürün Ekle", command=urun_ekle).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(form_frame, text="Ürün Sil", command=urun_sil).grid(row=3, column=2, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Toplam Tutar:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        toplam_tutar_entry = ttk.Entry(form_frame)
        toplam_tutar_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        toplam_tutar_entry.insert(0, "0.00")
        toplam_tutar_entry.config(state='readonly')
        
        ttk.Label(form_frame, text="Açıklama:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
        aciklama_text = scrolledtext.ScrolledText(form_frame, height=5, wrap=tk.WORD)
        aciklama_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        
        def kaydet():
            musteri_adi = musteri_combobox.get()
            musteri_id = None
            for m in musteriler:
                if (m['musteri_tipi'] == 'bireysel' and f"{m['ad']} {m['soyad']}" == musteri_adi) or \
                   (m['musteri_tipi'] == 'kurumsal' and m['firma_adi'] == musteri_adi):
                    musteri_id = m['id']
                    break
            if not musteri_id:
                messagebox.showerror("Hata", "Müşteri seçilmedi")
                return
            if not urunler_listesi:
                messagebox.showerror("Hata", "En az bir ürün ekleyin")
                return
            try:
                toplam_tutar = float(toplam_tutar_entry.get())
                satis_id = Musteri.satis_ekle(
                    musteri_id,
                    urunler_listesi,
                    toplam_tutar,
                    aciklama_text.get("1.0", tk.END).strip()
                )
                if satis_id:
                    messagebox.showinfo("Başarılı", "Satış eklendi")
                    pencere.destroy()
                    self.ana_ekran()
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir tutar girin")
        
        ModernButton(form_frame, text="Kaydet", command=kaydet).grid(row=6, column=0, columnspan=3, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        musteri_combobox.focus()
        pencere.bind('<Return>', lambda event: kaydet())

    def destek_talebi_ekrani(self):
        if not self.yetkiler.get('destek_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Destek Talebi")
        pencere.geometry("450x500")
        
        form_frame = ttk.Frame(pencere, style='Card.TFrame')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Müşteri:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        musteri_combobox = ttk.Combobox(form_frame,
                                       values=[f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi'] for m in Musteri.musterileri_listele()])
        musteri_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Konu:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        konu_entry = ttk.Entry(form_frame)
        konu_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Detay:").grid(row=2, column=0, padx=5, pady=5, sticky='ne')
        detay_text = scrolledtext.ScrolledText(form_frame, height=5, wrap=tk.WORD)
        detay_text.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Durum:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        durum_combobox = ttk.Combobox(form_frame, values=['açık', 'devam ediyor', 'kapalı'])
        durum_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        durum_combobox.set('açık')
        
        def kaydet():
            musteri_adi = musteri_combobox.get()
            musteri_id = None
            for m in musteriler:
                if (m['musteri_tipi'] == 'bireysel' and f"{m['ad']} {m['soyad']}" == musteri_adi) or \
                   (m['musteri_tipi'] == 'kurumsal' and m['firma_adi'] == musteri_adi):
                    musteri_id = m['id']
                    break
            if not musteri_id:
                messagebox.showerror("Hata", "Müşteri seçilmedi")
                return
            if not konu_entry.get():
                messagebox.showerror("Hata", "Konu girilmedi")
                return
            talep_id = Musteri.destek_talebi_olustur(
                musteri_id,
                konu_entry.get(),
                detay_text.get("1.0", tk.END).strip(),
                durum_combobox.get()
            )
            if talep_id:
                messagebox.showinfo("Başarılı", "Destek talebi oluşturuldu")
                pencere.destroy()
                self.ana_ekran()
        
        ModernButton(form_frame, text="Kaydet", command=kaydet).grid(row=4, column=0, columnspan=2, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        musteri_combobox.focus()
        pencere.bind('<Return>', lambda event: kaydet())

    def talep_durum_guncelle(self, tree):
        if not self.yetkiler.get('destek_yonetimi', False):
            messagebox.showerror("Hata", "Bu işlem için yetkiniz yok")
            return
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir talep seçin")
            return
        
        talep_id = int(tree.item(selected_item)['values'][0])
        pencere = tk.Toplevel(self.root)
        pencere.title("Talep Durum Güncelle")
        pencere.geometry("300x150")
        
        form_frame = ttk.Frame(pencere, style='Card.TFrame')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Yeni Durum:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        durum_combobox = ttk.Combobox(form_frame, values=['açık', 'devam ediyor', 'kapalı'])
        durum_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        def kaydet():
            durum = durum_combobox.get()
            if not durum:
                messagebox.showerror("Hata", "Durum seçilmedi")
                return
            if Destek.talep_durum_guncelle(talep_id, durum):
                messagebox.showinfo("Başarılı", "Talep durumu güncellendi")
                pencere.destroy()
                self.ana_ekran()
        
        ModernButton(form_frame, text="Güncelle", command=kaydet).grid(row=1, column=0, columnspan=2, pady=15, ipadx=20)
        form_frame.columnconfigure(1, weight=1)
        durum_combobox.focus()
        pencere.bind('<Return>', lambda event: kaydet())

    def musteri_satislar(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir müşteri seçin")
            return
        
        musteri_id = int(tree.item(selected_item)['values'][0])
        pencere = tk.Toplevel(self.root)
        pencere.title("Müşteri Satışları")
        pencere.geometry("900x600")
        
        columns = ("ID", "Ürünler", "Toplam Tutar", "Tarih", "Açıklama")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        tree.column("Ürünler", width=250, anchor='w')
        tree.column("Açıklama", width=250, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        satis_listesi = Satis.satis_listele(musteri_id)
        for s in satis_listesi:
            urunler_str = ", ".join([u['ad'] for u in s['urunler']])
            tree.insert('', tk.END,
                       values=(s['id'], urunler_str, f"{s['toplam_tutar']:.2f}",
                               s['tarih'], s['aciklama'] or ''))

    def musteri_destek_talepleri(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir müşteri seçin")
            return
        
        musteri_id = int(tree.item(selected_item)['values'][0])
        pencere = tk.Toplevel(self.root)
        pencere.title("Müşteri Destek Talepleri")
        pencere.geometry("900x600")
        
        columns = ("ID", "Konu", "Detay", "Durum", "Tarih", "Güncelleme Tarihi")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        tree.column("Konu", width=200, anchor='w')
        tree.column("Detay", width=250, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        talep_listesi = Destek.talep_listele(musteri_id)
        for t in talep_listesi:
            tree.insert('', tk.END,
                       values=(t['id'], t['konu'], t['detay'], t['durum'],
                               t['tarih'], t['guncelleme_tarihi'] or ''))

    def satis_raporu_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Satış Raporu")
        pencere.geometry("1000x700")
        
        filtre_frame = ttk.Frame(pencere, style='Card.TFrame')
        filtre_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filtre_frame, text="Başlangıç Tarihi (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        baslangic_entry = ttk.Entry(filtre_frame)
        baslangic_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filtre_frame, text="Bitiş Tarihi (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        bitis_entry = ttk.Entry(filtre_frame)
        bitis_entry.grid(row=0, column=3, padx=5, pady=5)
        
        def guncelle_rapor():
            baslangic = baslangic_entry.get()
            bitis = bitis_entry.get()
            try:
                if baslangic and bitis:
                    datetime.strptime(baslangic, "%Y-%m-%d")
                    datetime.strptime(bitis, "%Y-%m-%d")
                for widget in rapor_frame.winfo_children():
                    widget.destroy()
                
                musteriler_ad = []
                toplam_tutarlar = []
                satis_listesi = Satis.satis_listele(baslangic_tarihi=baslangic, bitis_tarihi=bitis)
                
                for m in musteriler:
                    musteri_satislar = [s for s in satis_listesi if s['musteri_id'] == m['id']]
                    toplam = sum(s['toplam_tutar'] for s in musteri_satislar)
                    if toplam > 0:
                        musteri_adi = f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi']
                        musteriler_ad.append(musteri_adi)
                        toplam_tutarlar.append(toplam)
                
                if not musteriler_ad:
                    ttk.Label(rapor_frame, text="Veri bulunamadı").pack(pady=20)
                    return
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                ax1.bar(musteriler_ad, toplam_tutarlar, color='#3B82F6')
                ax1.set_xlabel('Müşteriler')
                ax1.set_ylabel('Toplam Satış (TL)')
                ax1.set_title('Müşteri Bazında Satışlar')
                ax1.tick_params(axis='x', rotation=45)
                
                ax2.pie(toplam_tutarlar, labels=musteriler_ad, autopct='%1.1f%%', colors=['#3B82F6', '#10B981', '#F59E0B', '#EF4444'])
                ax2.set_title('Satış Dağılımı')
                
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=rapor_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir tarih formatı girin (YYYY-MM-DD)")
        
        ModernButton(filtre_frame, text="Raporu Güncelle", command=guncelle_rapor).grid(row=0, column=4, padx=5, pady=5)
        
        def rapor_disa_aktar():
            dosya = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Dosyası", "*.csv")])
            if dosya:
                with open(dosya, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Müşteri", "Toplam Tutar", "Satış Sayısı"])
                    for m in musteriler:
                        musteri_satislar = Satis.satis_listele(m['id'], baslangic_entry.get(), bitis_entry.get())
                        toplam = sum(s['toplam_tutar'] for s in musteri_satislar)
                        if toplam > 0:
                            musteri_adi = f"{m['ad']} {m['soyad']}" if m['musteri_tipi'] == 'bireysel' else m['firma_adi']
                            writer.writerow([musteri_adi, f"{toplam:.2f}", len(musteri_satislar)])
                messagebox.showinfo("Başarılı", "Rapor dışa aktarıldı")
        
        ModernButton(filtre_frame, text="CSV Olarak Dışa Aktar", command=rapor_disa_aktar).grid(row=0, column=5, padx=5, pady=5)
        
        rapor_frame = ttk.Frame(pencere)
        rapor_frame.pack(fill=tk.BOTH, expand=True)
        guncelle_rapor()

    def yedek_al(self):
        dosya = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dosyası", "*.json")])
        if dosya:
            Veritabani.veri_kaydet()
            with open(DATA_FILE, 'r', encoding='utf-8') as kaynak, open(dosya, 'w', encoding='utf-8') as hedef:
                hedef.write(kaynak.read())
            messagebox.showinfo("Başarılı", "Yedek alındı")

    def yedekten_yukle(self):
        dosya = tk.filedialog.askopenfilename(filetypes=[("JSON Dosyası", "*.json")])
        if dosya:
            try:
                with open(dosya, 'r', encoding='utf-8') as kaynak, open(DATA_FILE, 'w', encoding='utf-8') as hedef:
                    hedef.write(kaynak.read())
                Veritabani.veri_yukle()
                messagebox.showinfo("Başarılı", "Yedek yüklendi")
                self.ana_ekran()
            except Exception as e:
                messagebox.showerror("Hata", f"Yedek yüklenemedi: {e}")

    def kullanim_kilavuzu(self):
        messagebox.showinfo("Kullanım Kılavuzu", "Kılavuz için docs/kullanim_kilavuzu.md dosyasını okuyun.")

    def hakkinda(self):
        messagebox.showinfo("Hakkında", "CRM Sistemi\nSürüm: 2.1\nGeliştirici: Efe\nEn büyük BEŞİKTAŞ")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRMUygulamasi(root)
    root.mainloop()