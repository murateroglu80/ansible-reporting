import sys
import json
import csv

try:
    import pandas as pd
except ImportError:
    pd = None

def main():
    if len(sys.argv) < 4:
        print("Kullanım: python3 json_to_excel.py <input_json> <output_file> <format>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    out_format = sys.argv[3]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON okuma hatası: {e}")
        sys.exit(1)

    if not data:
        print("Dönüştürülecek veri bulunamadı (boş veri).")
        sys.exit(0)

    # Veriyi list of dicts formatına getir
    if isinstance(data, dict):
        data = [data]

    if out_format == 'csv':
        keys = set()
        for item in data:
            keys.update(item.keys())
        keys = list(keys)

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Başarıyla kaydedildi: {output_file}")
        except Exception as e:
            print(f"CSV yazma hatası: {e}")
            sys.exit(1)

    elif out_format == 'excel':
        if pd is None:
            print("[HATA] Excel dönüşümü için pandas kütüphanesi gerekli.")
            print("Lütfen kontrol makinesine şu kütüphaneleri kurun: pip install pandas openpyxl")
            sys.exit(1)
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(output_file, index=False)
            print(f"Başarıyla kaydedildi: {output_file}")
        except Exception as e:
            print(f"Excel yazma hatası: {e}")
            sys.exit(1)
    else:
        print(f"Sadece 'csv' veya 'excel' formatları destekleniyor (Format: {out_format}). JSON formatı zaten Ansible tarafından kaydediliyor.")

if __name__ == '__main__':
    main()
