📋 Gelişmiş CRM Sistemi
Gelişmiş CRM Sistemi, müşteri ilişkileri yönetimi (CRM) süreçlerini kolaylaştırmak için tasarlanmış, kullanıcı dostu bir uygulamadır. Python ve Tkinter kullanılarak geliştirilen bu sistem, müşteri yönetimi, satış takibi, destek talebi yönetimi ve raporlama gibi temel işlevleri sunar. Küçük ve orta ölçekli işletmeler için ideal bir çözümdür.

🚀 Özellikler

Kullanıcı Yönetimi:
Kullanıcı kaydı ve giriş sistemi (SHA-256 şifreleme).
Yetki bazlı erişim kontrolü (müşteri, satış, destek yönetimi).
Son giriş tarihi takibi.


Müşteri Yönetimi:
Bireysel ve kurumsal müşteri ekleme, düzenleme, silme.
Telefon, e-posta, adres ve notlar gibi detaylı bilgi girişi.
Vergi numarası doğrulaması (kurumsal müşteriler için).
Arama ve filtreleme ile müşteri listeleme.


Satış Yönetimi:
Satış kaydı oluşturma (ürün ekleme, toplam tutar hesaplama).
Müşteri bazlı satış geçmişi görüntüleme.
Açıklama ekleme ve satış detaylarını düzenleme.


Destek Talebi Yönetimi:
Müşteri adına destek talebi oluşturma.
Talep durumu güncelleme (açık, devam ediyor, kapalı).
Müşteri bazlı destek talebi listeleme.


Raporlama:
Satış raporları (grafiksel: çubuk ve pasta grafiği).
Raporları CSV formatında dışa aktarma.


Veri Yönetimi:
JSON formatında veri depolama.
Otomatik yedekleme (her 10 dakikada bir).
Manuel yedek alma ve yedekten yükleme.


Kullanıcı Arayüzü:
Modern Tkinter tabanlı arayüz (açık/koyu tema desteği).
Sekmeli yapı (müşteriler, satışlar, destek talepleri).
Hızlı erişim butonları ve sağ tık menüsü.


Ek Özellikler:
Kısayol tuşları (örneğin, Ctrl+M ile müşteri ekleme).
Durum çubuğu (aktif kullanıcı ve son giriş bilgisi).




🛠 Kurulum
Gereksinimler

Python 3.6 veya üzeri
Tkinter (genellikle Python ile birlikte gelir)
Matplotlib (grafikler için)
Standart Python kütüphaneleri (json, hashlib, csv, os, datetime, re, threading)

Kurulum Adımları

Depoyu Klonlayın veya İndirin:
git clone https://github.com/kullanici/crm-sistemi.git

veya ZIP dosyasını indirip çıkarın.

Proje Dizinine Gidin:
cd crm-sistemi


Gerekli Kütüphaneleri Yükleyin:

Tkinter genellikle Python ile birlikte gelir. Emin olmak için şu komutu çalıştırın:python -c "import tkinter"

Eğer hata alırsanız, Tkinter'ı yükleyin:
Ubuntu/Debian: sudo apt-get install python3-tk
Windows/macOS: Genellikle Python kurulumunda bulunur.


Matplotlib kütüphanesini yükleyin:pip install matplotlib




Uygulamayı Çalıştırın:
python crm.denem.py




📚 Kullanım
1. Giriş Yapma veya Kayıt Olma

<img src="https://github.com/Ahmet1408/crm_app/blob/main/crm/ss/login.png" alt="login">

Giriş Ekranı:
Varsayılan kullanıcı: admin / Şifre: 12345
Yeni kullanıcı oluşturmak için "Yeni Kullanıcı Kaydı" butonuna tıklayın.
Kullanıcı adı, şifre ve yetkileri (müşteri/satış/destek yönetimi) belirleyerek kayıt olun.
Kayıt olduktan sonra giriş yapın.


Not: Şifreler SHA-256 ile şifrelenir ve güvenli bir şekilde saklanır.

2. Ana Ekran


<img src="https://github.com/Ahmet1408/crm_app/blob/main/crm/ss/main.png" alt="main">

Menü Çubuğu:
Dosya: Yedek al, yedekten yükle, tema değiştir, çıkış.
İşlemler: Müşteri ekle, satış ekle, destek talebi oluştur.
Raporlar: Satış raporu.
Yardım: Kullanım kılavuzu, hakkında.


Sol Panel:
Hızlı erişim butonları (Müşteri Ekle, Satış Ekle, Destek Talebi, Satış Raporu).
Son eklenen 5 müşteri listesi.


Sağ Panel:
Sekmeler: Müşteriler, Satışlar, Destek Talepleri.


Durum Çubuğu:
Aktif kullanıcı adı ve son giriş zamanı.



3. Müşteri Yönetimi

<img src="https://github.com/Ahmet1408/crm_app/blob/main/crm/ss/musteri_ekle.png" alt="musteri_ekle">

Müşteri Ekle:
Menüden veya hızlı erişim butonundan "Müşteri Ekle"yi seçin (Ctrl+M).
Bireysel veya kurumsal müşteri tipini seçin.
Gerekli bilgileri (ad, soyad, firma adı, telefon, e-posta, adres, notlar, vergi no) girin.


Müşteri Düzenle/Sil:
Müşteri listesinde bir müşteriye sağ tıklayın.
"Düzenle" veya "Sil" seçeneklerini kullanın.


Arama:
Müşteri sekmesinde arama çubuğunu kullanarak müşterileri filtreleyin.



4. Satış Yönetimi

<img src="https://github.com/Ahmet1408/crm_app/blob/main/crm/ss/sat%C4%B1s_ekle.png" alt="satıs_yonetim">


Satış Ekle:
Menüden veya hızlı erişim butonundan "Satış Ekle"yi seçin (Ctrl+S).
Müşteri seçin, ürünleri ekleyin (ürün adı ve fiyat), toplam tutar otomatik hesaplanır.
Açıklama ekleyip kaydedin.


Satışları Görüntüle:
Müşteri listesinden bir müşteriye sağ tıklayın ve "Satışları Görüntüle"yi seçin.



5. Destek Talebi Yönetimi

Destek Talebi Oluştur:
Menüden veya hızlı erişim butonundan "Destek Talebi Oluştur"u seçin (Ctrl+D).
Müşteri, konu, detay ve durum bilgilerini girin.


Durum Güncelle:
Destek talebi listesinde bir talebe sağ tıklayın ve "Durum Güncelle"yi seçin.


Talepleri Görüntüle:
Müşteri listesinden bir müşteriye sağ tıklayın ve "Destek Talepleri"ni seçin.



6. Raporlama ve Yedekleme

Satış Raporu:
Menüden veya hızlı erişim butonundan "Satış Raporu"nu seçin.
Tarih aralığı girerek müşteri bazında satış grafiklerini (çubuk ve pasta) görüntüleyin.
Raporu CSV formatında dışa aktarın.


Yedekleme:
Otomatik yedekleme her 10 dakikada bir yapılır.
Manuel olarak "Yedek Al" ile JSON formatında yedek alabilirsiniz.
"Yedekten Yükle" ile verileri geri yükleyin.



7. Tema Değiştirme

Menüden "Dosya > Tema Değiştir" seçeneği ile açık ve koyu tema arasında geçiş yapın.


⚙️ Teknik Detaylar

Dil: Python 3
Arayüz: Tkinter
Grafikler: Matplotlib
Veri Depolama: JSON dosyası (crm_data.json)
Şifreleme: SHA-256
Dosya Formatı: JSON (yedekleme), CSV (rapor dışa aktarma)
Yetki Seviyeleri:
Müşteri Yönetimi
Satış Yönetimi
Destek Yönetimi





📧 İletişim
Sorularınız veya önerileriniz için:

E-posta: efe.ahmet@netline.net.tr
