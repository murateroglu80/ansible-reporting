import json
from ansible.utils.display import Display

display = Display()

def custom_filter(data, filters, host_name="unknown"):
    """
    Gelen veriyi (JSON veya Düz Metin) belirtilen kurallara göre filtreler ve yapılandırır.
    data: string, dict veya list of dicts
    filters: list of dicts (column, operator, value)
    host_name: İşlemin yapıldığı sunucunun adı (Sütun olarak eklenecek)
    """
    if not data:
        return []
        
    if isinstance(data, str):
        try:
            # Önce JSON formatında mı diye dene
            data = json.loads(data)
        except Exception:
            # JSON değilse, gelen metni satır satır okuyup SÜTUNLARA (Dictionary) çevir
            parsed_dict = {"Sunucu": host_name}
            lines = data.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or line.lower().startswith('copyright'):
                    continue
                
                # Eğer satırda ':' varsa, bunu "Sütun_Adı : Değer" olarak ayır
                if ':' in line:
                    parts = line.split(':', 1)
                    key = parts[0].strip()
                    val = parts[1].strip()
                    parsed_dict[key] = val
                else:
                    # İki nokta olmayan satırları (örn: Trellix Endpoint Security...) Ürün Adı sütununa koy
                    parsed_dict["Urun_Adi"] = line
                    
            data = [parsed_dict]

    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        return []

    # Eğer filtreleme özelliği kapalıysa veriyi filtrelemeden direkt döndür
    if not filters:
        return data

    filtered_data = []
    
    for row in data:
        if not isinstance(row, dict):
            continue
            
        passed = True
        for f in filters:
            column = f.get('column')
            operator = f.get('operator')
            value = f.get('value')

            if column not in row:
                passed = False
                break
            
            row_val = row[column]
            
            if operator == '>':
                try:
                    if float(row_val) <= float(value):
                        passed = False
                        break
                except (ValueError, TypeError):
                    display.warning(f"[UYARI] '{column}' kolonu numerik değil ('{row_val}'), > operatörü uygulanamaz!")
                    passed = False
                    break
            elif operator == '<':
                try:
                    if float(row_val) >= float(value):
                        passed = False
                        break
                except (ValueError, TypeError):
                    display.warning(f"[UYARI] '{column}' kolonu numerik değil ('{row_val}'), < operatörü uygulanamaz!")
                    passed = False
                    break
            elif operator in ('=', '=='):
                if str(row_val) != str(value):
                    passed = False
                    break
            elif operator == 'contains':
                if str(value).lower() not in str(row_val).lower():
                    passed = False
                    break
            else:
                display.warning(f"[UYARI] Bilinmeyen operatör '{operator}'")
                passed = False
                break
        
        if passed:
            filtered_data.append(row)

    return filtered_data

class FilterModule(object):
    def filters(self):
        return {
            'custom_filter': custom_filter
        }
