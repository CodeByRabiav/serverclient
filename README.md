# Basit Sunucu-İstemci Uygulaması (Server - Client)

Basit bir sunucu ve istemci uygulaması.İstemci, metinleri çeşitli şifreleme yöntemleriyle şifreleyip sunucuya gönderebilir; ayrıca dosya gönderimi de desteklenir. Sunucu gelen veriyi alır, metin dosyalarını arayüzde gösterir.

## Nasıl Çalıştırılır?

1. Depoyu bilgisayarına klonla veya dosyaları indir.
2. Terminal veya komut satırını aç.
3. Sunucuyu başlat:
   ```bash
   python server.py

4. ardından başka bir terminal açarak istemciyi başlatın:
    ```bash
   python client.py

5. İstemci arayüzünden:

   Şifreleme yöntemini seç.
   Anahtarı ve metni gir.
   “Şifrele ve Gönder” butonuna tıkla.
   Dosya göndermek istersen “Dosya Gönder” butonunu kullan.

## ekran görüntüleri

![Sunucu Arayüzü](serverclient1/screenshots/server.png)
![İstemci Arayüzü](serverclient1/screenshots/client.png)
![Gönderme Sonucu](serverclient1/screenshots/result.png)

## kullanılan teknolojiler

    socket (iletişim)

    tkinter (grafik arayüz)

    threading (çoklu bağlantı desteği)