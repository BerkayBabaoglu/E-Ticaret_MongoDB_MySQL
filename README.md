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
