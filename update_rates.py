import json
import os
import urllib.request

def update_rates():
    # 1. Отримуємо актуальні курси відносно USD
    # Використовуємо USD як базу, бо зазвичай всі курси рахуються через нього
    url = "https://open.er-api.com/v6/latest/USD"
    print("Отримання актуальних курсів валют...")
    try:
        with urllib.request.urlopen(url) as response:
            rates_data = json.loads(response.read())
            rates = rates_data.get("rates", {})
    except Exception as e:
        print(f"❌ Помилка API: {e}")
        return

    if not rates:
        print("❌ Не вдалося отримати курси валют.")
        return

    # 2. Пошук усіх мовних файлів у папці i18n
    i18n_dir = 'i18n'
    if not os.path.exists(i18n_dir):
        print(f"❌ Папка {i18n_dir} не знайдена.")
        return

    lang_files = [f for f in os.listdir(i18n_dir) if f.endswith('.json')]
    
    for file_name in lang_files:
        file_path = os.path.join(i18n_dir, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
            
            code = lang_data.get('currency_code')
            old_rate = lang_data.get('exchange_rate')

            # 3. Перевірка та оновлення курсу
            if code and code in rates:
                # API дає курс відносно USD (наприклад, 1 USD = 41 UAH)
                new_rate = round(rates[code], 2)
                
                if old_rate != new_rate:
                    lang_data['exchange_rate'] = new_rate
                    
                    # Зберігаємо оновлений файл
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(lang_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ {file_name} ({code}): {old_rate} -> {new_rate}")
                else:
                    print(f"ℹ️ {file_name} ({code}): курс не змінився ({old_rate})")
            else:
                print(f"⚠️ {file_name}: код валюти '{code}' не знайдено в API")
                
        except Exception as e:
            print(f"❌ Помилка при обробці {file_name}: {e}")

    print("\nПроцес оновлення завершено.")

if __name__ == "__main__":
    update_rates()
    
