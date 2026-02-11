import json
import os
import shutil

BASE_PATH = "/stop_pay"

def load_template(template_name):
    path = f'templates/{template_name}'
    if not os.path.exists(path):
        print(f"❌ ПОМИЛКА: Шаблон {path} не знайдено!")
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def build():
    print("🚀 Початок збирання...")
    
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    os.makedirs('dist', exist_ok=True)
    print("✅ Папка dist підготовлена")

    if os.path.exists('assets'):
        shutil.copytree('assets', 'dist/assets', dirs_exist_ok=True)
        print("✅ Assets скопійовано")
    
    root_files = ['manifest.json', 'favicon-32x32.png', 'apple-touch-icon.png', 'Logo.png', 'data.json']
    for rf in root_files:
        if os.path.exists(rf):
            shutil.copy(rf, f'dist/{rf}')

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            site_data = json.load(f)
    except Exception as e:
        print(f"❌ ПОМИЛКА завантаження data.json: {e}")
        return

    languages = [lang.lower() for lang in site_data['languages'].keys()]
    print(f"🌍 Знайдено мови: {languages}")
    
    layout = load_template('layout.html')
    if not layout: return

    for lang in languages:
        lang_dir = f'dist/{lang}'
        os.makedirs(lang_dir, exist_ok=True)
        
        # Головна сторінка мови
        lang_upper = lang.upper()
        main_info = site_data['languages'][lang_upper]
        main_content = f'<div id="siteContent"></div>' # Спрощено для тесту
        
        index_html = layout.replace('{{ content }}', main_content)
        index_html = index_html.replace('href="/', f'href="{BASE_PATH}/').replace('src="/', f'src="{BASE_PATH}/')
        
        with open(f'{lang_dir}/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"📄 Створено: {lang_dir}/index.html")

        # Сервіси
        if os.path.exists('services'):
            service_files = [f for f in os.listdir('services') if f.endswith('.json')]
            print(f"📦 Знайдено сервісів: {len(service_files)} для {lang}")
            
            for s_file in service_files:
                content_path = f'content/{lang}/{s_file}'
                if os.path.exists(content_path):
                    # Тут логіка створення сторінки (як у тебе)
                    service_dir = f'dist/{lang}/{s_file.replace(".json", "")}'
                    os.makedirs(service_dir, exist_ok=True)
                    with open(f'{service_dir}/index.html', 'w', encoding='utf-8') as f:
                        f.write("test content")
                    print(f"   ✅ Створено сторінку сервісу: {s_file}")
                else:
                    print(f"   ⚠️ Відсутній контент для {s_file} мовою {lang} (шукав у {content_path})")

    # Редірект
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write("<html><script>window.location.href='/stop_pay/ua/'</script></html>")
    print("✅ Створено головний редірект dist/index.html")

if __name__ == "__main__":
    build()
    
