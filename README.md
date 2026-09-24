# Ansible Reporting Automation

Bu proje, uzak sunucularda çalıştırılan komutların ürettiği JSON formatındaki çıktıları merkezi olarak toplayan, özel filtreleme kurallarından geçiren ve bu veriyi JSON, CSV veya Excel formatında konsolide bir rapor haline getiren bir otomasyon sistemidir.

Bash history'de komut parametreleri veya hassas verilerin gözükmemesi için tüm yapılandırma ve komut ayarları ayrı bir `config.yml` dosyasından okunmaktadır.

## 🚀 Özellikler

- **Dinamik Veri Çekme:** Sunuculardan (host) gelen çıktıları otomatik JSON'a çevirir.
- **Gelişmiş Filtreleme:** `<`, `>`, `=`, `contains` gibi operatörleri destekleyen özel bir Python eklentisine sahiptir. Tip uyuşmazlığında uyarı (warning) verir ve süreci kesintiye uğratmaz.
- **Güvenlik:** Tüm parametreler ve komut yapıları playbook dışında tutulduğu için terminal geçmişinde veya loglarda hiçbir argüman izi bırakmaz.
- **Çoklu Çıktı Formatı:** Sonuçları doğrudan **JSON**, **CSV**, **Excel** formatına dönüştürebilir veya dosya oluşturmadan doğrudan **Ekrana (Console)** basabilirsiniz (`none` seçeneği).
- **Esnek Filtreleme Toggle:** İhtiyacınıza göre filtreleri tek bir ayarla tamamen kapatıp (`enable_filters: false`) tüm veriyi ham haliyle işleyebilirsiniz.

## 📦 Gereksinimler

- **Ansible** (Control Node üzerinde kurulu olmalı)
- **Python 3.x**
- Excel çıktılarına ihtiyaç duyuyorsanız, Control Node (Raporu oluşturduğunuz makine) üzerinde `pandas` ve `openpyxl` kurulu olmalıdır:
  ```bash
  pip install pandas openpyxl
  ```

## 🛠️ Kurulum ve Ayarlama

1. **Repoyu Klonlayın:**
   ```bash
   git clone https://github.com/murateroglu80/ansible-reporting.git
   cd ansible-reporting
   ```

2. **Envanteri Ayarlayın (`inventory.ini`):**
   Hedef sunucularınızı `inventory.ini` dosyasına ekleyin.
   ```ini
   [all]
   sunucu1 ansible_host=192.168.1.10
   sunucu2 ansible_host=192.168.1.11
   ```
   *(Varsayılan olarak projeyi doğrudan test edebilmeniz için localhost eklidir.)*

3. **Komut ve Filtreleri Belirleyin (`config.yml`):**
   Bu dosya, otomasyonun beynidir. Hangi komutun çalıştırılacağı, verinin nasıl filtreleneceği ve hangi formatta rapor istendiği buradan belirlenir.
   
   ```yaml
   target_command: "/opt/bin/command -c" # Sunucularda çalıştırılacak asıl komut
   output_format: "none"                 # Seçenekler: json, csv, excel, none
   
   enable_filters: false                 # Filtreleri açıp kapatmak için (true/false)
   
   filters:
     - column: "status"
       operator: "contains"
       value: "active"
     - column: "cpu_usage"
       operator: ">"
       value: 80.5
   ```

## ▶️ Kullanım

Tüm ayarları tamamladıktan sonra playbook'u aşağıdaki gibi temiz bir şekilde çalıştırabilirsiniz:

```bash
ansible-playbook rapor.yml
```

### 📋 Beklenen Sonuçlar
- Eğer veriler filtrelerden başarıyla geçerse `output/` klasörünün içinde konsolide edilmiş tüm sunucuların sonuçları oluşturulur.
- İstediğiniz hedef formata göre (`output_format` parametresi) `konsolide_rapor.json`, `konsolide_rapor.csv` veya `konsolide_rapor.xlsx` isimli dosya Control Node üzerinde (output klasöründe) oluşturulur. Eğer **`none`** formati seçtiyseniz, dosya oluşturulmaz, tüm sonuç doğrudan ekrana okunaklı bir şekilde yazdırılır.
- Numerik olmayan bir veriye (örn. `"N/A"`) `>` veya `<` ile işlem yapılmaya çalışıldığında Ansible ekranında süreci bozmayan güvenli bir uyarı görürsünüz:
  `[UYARI] 'cpu_usage' kolonu numerik değil ('N/A'), > operatörü uygulanamaz!`

## 📁 Proje Yapısı

```text
├── ansible.cfg                # Ansible yapılandırması (Eklenti yolunu belirtir)
├── inventory.ini              # Host tanımları
├── config.yml                 # KULLANICININ DÜZENLEYECEĞİ DOSYA (Komut ve Filtreler)
├── rapor.yml                  # ANA PLAYBOOK
├── filter_plugins/            # Gelişmiş filtreleme için Python kodları
│   └── custom_filters.py      # Operatör ve Numeric kontrollerini yapan eklenti
├── scripts/
│   └── json_to_excel.py       # JSON'u Excel/CSV formatına dönüştürücü
└── output/                    # Çıktıların toplanacağı klasör (Git'e dahil edilmez)
```
