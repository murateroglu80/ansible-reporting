Ansible Komut Çıktısı İşleme ve Raporlama Planı (V2 - Güncellenmiş)
Kullanıcı geri bildirimlerine göre güncellenmiş nihai mimari ve iş akışı aşağıdadır.

1. Mimari ve İş Akışı
Güvenli ve Temiz Girdi Yönetimi (Bash History Koruması):

Komut satırında uzun parametreler kullanılmayacaktır. Tüm ayarlar (çalıştırılacak komut, filtreleme kriterleri, istenen format) harici bir config.yml dosyasından okunacaktır.
Playbook sadece ansible-playbook rapor.yml şeklinde tertemiz çalıştırılacak, böylece bash history'de hiçbir hassas veri (komut veya parametre) görünmeyecektir.
Veri Toplama (JSON Tabanlı):

Uzak sunucularda config.yml içindeki komut çalıştırılır.
Komutun zaten JSON formatında döndürdüğü çıktı, Ansible'ın from_json filtresi ile doğrudan yapılandırılmış bir sözlük (dictionary) objesine dönüştürülür.
Gelişmiş Filtreleme ve Tip Kontrolü (Custom Python Filter Plugin):

İhtiyaç: =, >, <, contains gibi operatörleri desteklemek ve sayısal (numeric) olmayan bir veriye büyüktür/küçüktür işlemi yapılmaya çalışıldığında uyarı vermek.
Çözüm: Bu kadar dinamik bir mantığı saf Ansible (Jinja2) ile yapmak hantal ve kısıtlıdır. Bunun yerine, Ansible'ın içine ufak bir özel filtre (Custom Filter Plugin) yazılacaktır.
Bu eklenti:
Gelen veriyi tarar.
config.yml'daki kuralları işletir.
Tip uyuşmazlığı varsa (örn: isim > 5) ekrana/loglara anlaşılır bir uyarı (warning) basar ve o satırı atlar.
Konsolide Raporlama ve Dışa Aktarma:

Tüm sunuculardan (host) gelen JSON veriler Control Node (Ansible'ı çalıştıran makine) üzerinde tek bir listede (array) birleştirilir.
JSON Çıktı: Birleştirilen veri doğrudan konsolide_rapor.json olarak kaydedilir.
CSV Çıktı: JSON veri Jinja2 veya Python modülü ile tabloya dönüştürülerek konsolide_rapor.csv olarak kaydedilir.
Excel (XLSX) Dönüşümü: Excel formatı istendiğinde, Ansible localhost üzerinde ufak bir Python scriptini (veya modülünü) tetikleyerek oluşturulan JSON veya CSV dosyasını tam teşekküllü bir Excel dosyasına (konsolide_rapor.xlsx) dönüştürür.
2. Dizin Yapısı (Oluşturulacak Dosyalar)
text

ansible_projesi/
├── ansible.cfg                # Custom filter eklentilerinin yolunu belirtir
├── inventory.ini              # Host tanımları ve How-To belgesi referansları
├── config.yml                 # KULLANICININ DÜZENLEYECEĞİ DOSYA (Komut ve Filtreler)
├── rapor.yml                  # ANA PLAYBOOK
├── filter_plugins/            # Gelişmiş filtreleme ve tip kontrolü için Python kodları
│   └── custom_filters.py      # Operatör ve Numeric kontrollerini yapacak eklenti
├── scripts/
│   └── json_to_excel.py       # JSON verisini Excel'e dönüştürecek çevirici araç
└── output/                    # Çıktıların (JSON, CSV, XLSX) toplanacağı klasör
3. Örnek Kullanım Senaryosu (Kurgu)
1. Kullanıcı config.yml dosyasını düzenler:

yaml

target_command: "/opt/bin/command -c"
output_format: "excel" # Seçenekler: json, csv, excel
filters:
  - column: "status"
    operator: "contains"
    value: "active"
  - column: "cpu_usage"
    operator: ">"
    value: 80.5
2. Playbook Çalıştırılır:

bash

ansible-playbook rapor.yml
3. Beklenen Sonuçlar:

Eğer cpu_usage alanında string ("N/A" gibi) bir veri gelirse sistem: [UYARI] 'cpu_usage' kolonu numerik değil, > operatörü uygulanamaz! şeklinde uyarı verir.
Başarılı eşleşmeler output/konsolide_rapor.xlsx (ve referans için .json formatında) Control Node'da oluşturulur.
