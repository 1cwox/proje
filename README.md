# Flask Aşk Sitesi

Bu proje, çiftler için hazırlanmış, özelleştirilebilir ve estetik bir aşk web sitesidir. Flask ile yazılmıştır.

## Özellikler
- Tüm içerik Python tarafında yönetilir
- Galeriye ve timeline'a admin olarak ekleme/silme
- Profil fotoğraflarını admin olarak güncelleme
- Responsive ve modern tasarım

## Kurulum
1. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```
2. Uygulamayı başlatın:
   ```
   python app.py
   ```
3. Admin girişi için `/admin` adresini kullanın (varsayılan: admin/1234).

## Render.com Deploy
- Projeyi GitHub'a yükleyin.
- `Procfile` ve `requirements.txt` dosyalarını ekleyin.
- Render.com'da yeni Web Service oluşturun ve repoyu bağlayın.

## Notlar
- Profil fotoğrafları: `static/profiles/` klasöründe `kiz.jpg` ve `erkek.jpg` olarak bulunmalı.
- Galeri fotoğrafları: `static/uploads/` klasöründe saklanır.
- Timeline olayları `timeline.json` dosyasında saklanır. 