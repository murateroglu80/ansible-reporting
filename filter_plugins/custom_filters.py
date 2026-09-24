from ansible.utils.display import Display

display = Display()

def custom_filter(data, filters):
    """
    Gelen JSON verisini belirtilen kurallara göre filtreler.
    data: dict veya list of dicts
    filters: list of dicts (column, operator, value)
    """
    if not data:
        return []
        
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        return []

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
