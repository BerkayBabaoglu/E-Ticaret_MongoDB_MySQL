# HibritDB

HibritDB, Django framework'ü kullanılarak geliştirilmiş bir web uygulamasıdır.

## Proje Hakkında

Bu proje, veritabanı yönetimi ve web arayüzü entegrasyonunu sağlayan bir hibrit veritabanı yönetim sistemidir.

## Kurulum Aşamaları

### Gereksinimler
- Python 3.x
- pip (Python paket yöneticisi)
- Virtual environment (önerilen)

### Kurulum Adımları

1. Projeyi klonlayın:
```bash
git clone [repo-url]
cd HibritDB
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv .venv
# Windows için:
.venv\Scripts\activate
# Linux/Mac için:
source .venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanı migrasyonlarını uygulayın:
```bash
python manage.py migrate
```

5. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

6. Tarayıcınızda `http://127.0.0.1:8000` adresine giderek uygulamayı görüntüleyebilirsiniz.

## Proje Yapısı
HibritDB/
├── .venv/ # Sanal ortam dosyaları
├── HibritDB/ # Ana proje dizini
├── static/ # Statik dosyalar (CSS, JS, resimler)
├── templates/ # HTML şablonları
├── db.sqlite3 # Veritabanı dosyası
└── manage.py # Django yönetim komutları

##Projenin Görselleri
![Ekran görüntüsü 2025-04-28 090540](https://github.com/user-attachments/assets/9f3291f7-b67e-4737-9145-179297e31d9a)
![Ekran görüntüsü 2025-04-28 090555](https://github.com/user-attachments/assets/59acef8b-877a-4826-8e38-ff8195ac29d8)
![Ekran görüntüsü 2025-04-28 090519](https://github.com/user-attachments/assets/ddafbcff-229a-4a79-8cca-57eaf7f60cbc)
![Ekran görüntüsü 2025-04-28 090647](https://github.com/user-attachments/assets/9145044e-9ebb-46c8-96d3-f39c9db87545)

##Kullanılan Teknolojiler
- Django
- SQLite
- HTML/CSS
- JavaScript

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun
