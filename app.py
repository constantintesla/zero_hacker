from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from datetime import timedelta
import os
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import random
import time
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "matrix-green")
app.permanent_session_lifetime = timedelta(hours=6)

TARGET_HOST = "http://138.124.81.201/"

# Генерируем случайный зашифрованный IP для декодирования
ENCRYPTED_IP = "4A.3B.2C.1D"  # Будет заменен на реальный зашифрованный IP
REAL_IP = "192.168.1.100"  # Реальный IP для проверки

# Админ настройки
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "matrix2024")

# Настройки заданий (будут управляться через админку)
TASK_SETTINGS = {
    'watermark': {
        'enabled': True,
        'required_brightness': 60,  # Снижено с 80
        'required_contrast': 70,    # Снижено с 85
        'required_gamma': 50,       # Снижено с 75
        'required_saturation': 60,  # Снижено с 90
        'required_hue': 40,        # Снижено с 60
        'hidden_message': 'ZERO_HACKER_2024',
        'password_for_next': 'HACK_LEVEL_2'
    },
    'hack_simulation': {
        'enabled': True,
        'duration_minutes': 20,
        'encrypted_ip': 'XYZ.WVU.TS.RQP',
        'real_ip': '138.124.81.201',
        'progress_phases': [
            'Сканирование портов...',
            'Поиск уязвимостей...',
            'Взлом системы...',
            'Извлечение данных...',
            'Шифрование IP адреса...'
        ]
    },
    'ip_decode': {
        'enabled': True,
        'encrypted_ip': 'XYZ.WVU.TS.RQP',
        'real_ip': '138.124.81.201',
        'decoder_steps': 11
    }
}

@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html", target_host=TARGET_HOST)

@app.route("/watermark", methods=["GET", "POST"])
def watermark_task():
    if request.method == "POST":
        # Обработка загруженного изображения
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Создаем изображение с невидимой водяной меткой
                img = Image.open(file.stream)
                img_with_watermark = add_invisible_watermark(img)
                
                # Конвертируем в base64 для отправки клиенту
                buffered = io.BytesIO()
                img_with_watermark.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                return jsonify({"success": True, "image": img_str})
    
    return render_template("watermark.html")

@app.route("/watermark/default")
def get_default_image():
    """Возвращает изображение по умолчанию"""
    try:
        # Пытаемся загрузить предобработанное изображение Вовы
        image_path = "static/images/vova_watermarked.jpg"
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
                img_str = base64.b64encode(img_data).decode()
                return jsonify({"success": True, "image": img_str})
        else:
            return jsonify({"success": False, "error": "Default image not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/hack", methods=["GET", "POST"])
def hack_simulation():
    if request.method == "POST":
        password = request.form.get('password', '')
        # Проверяем пароль из первого задания
        if password == TASK_SETTINGS['watermark']['password_for_next']:
            session['hack_authenticated'] = True
            return redirect(url_for('hack_dashboard'))
        else:
            flash('Неверный пароль! Получите пароль, выполнив первое задание.', 'error')
    
    return render_template('hack_login.html')

@app.route('/hack/dashboard')
def hack_dashboard():
    if not session.get('hack_authenticated'):
        return redirect(url_for('hack_simulation'))
    return render_template('hack_dashboard.html')

@app.route("/decode", methods=["GET", "POST"])
def decode_ip():
    if request.method == "POST":
        password = request.form.get('password', '')
        # Проверяем пароль из второго задания
        if password == 'HACK_COMPLETE':  # Пароль из хакерской атаки
            session['decode_authenticated'] = True
            return redirect(url_for('decode_dashboard'))
        else:
            flash('Неверный пароль! Получите пароль, выполнив второе задание.', 'error')
    
    return render_template('decode_login.html')

@app.route('/decode/dashboard')
def decode_dashboard():
    if not session.get('decode_authenticated'):
        return redirect(url_for('decode_ip'))
    return render_template('ip_decode.html')

@app.route("/end", methods=["GET"]) 
def end():
    return render_template("end.html", target_host=TARGET_HOST)

# Админ маршруты
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Неверные учетные данные', 'error')
    
    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template("admin/dashboard.html", settings=TASK_SETTINGS)

@app.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == "POST":
        # Обработка изменения пароля админки
        new_username = request.form.get('admin_username', '').strip()
        new_password = request.form.get('admin_password', '').strip()
        password_confirm = request.form.get('admin_password_confirm', '').strip()
        
        if new_username:
            global ADMIN_USERNAME
            ADMIN_USERNAME = new_username
        
        if new_password:
            if new_password != password_confirm:
                flash('Пароли не совпадают!', 'error')
                return redirect(url_for('admin_settings'))
            if len(new_password) < 4:
                flash('Пароль должен содержать минимум 4 символа!', 'error')
                return redirect(url_for('admin_settings'))
            global ADMIN_PASSWORD
            ADMIN_PASSWORD = new_password
            flash('Пароль админки изменен!', 'success')
        
        # Обновляем настройки заданий
        for task_name, task_data in TASK_SETTINGS.items():
            for key, value in task_data.items():
                form_key = f"{task_name}_{key}"
                if form_key in request.form:
                    if key == 'enabled':
                        # Для чекбоксов enabled
                        TASK_SETTINGS[task_name][key] = True
                    elif key in ['required_brightness', 'required_contrast', 'required_gamma', 'required_saturation', 'required_hue', 'duration_minutes', 'decoder_steps']:
                        TASK_SETTINGS[task_name][key] = int(request.form.get(form_key))
                    else:
                        TASK_SETTINGS[task_name][key] = request.form.get(form_key)
                elif key == 'enabled':
                    # Если чекбокс не отмечен, устанавливаем False
                    TASK_SETTINGS[task_name][key] = False
        
        # Обработка фаз прогресса для хакерской симуляции
        progress_phases = []
        for key, value in request.form.items():
            if key.startswith('hack_simulation_progress_phases_'):
                progress_phases.append(value)
        if progress_phases:
            TASK_SETTINGS['hack_simulation']['progress_phases'] = progress_phases
        
        flash('Настройки обновлены!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template("admin/settings.html", settings=TASK_SETTINGS, admin_username=ADMIN_USERNAME)

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route("/admin/upload-watermark-image", methods=["POST"])
def upload_watermark_image():
    """Загружает новое изображение по умолчанию для задания с водяными знаками"""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Unauthorized"})
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            try:
                # Обрабатываем изображение и добавляем водяную метку
                img = Image.open(file.stream)
                img_with_watermark = add_invisible_watermark(img)
                
                # Сохраняем как новое изображение по умолчанию
                output_path = "static/images/vova_watermarked.jpg"
                if img_with_watermark.mode == 'RGBA':
                    img_with_watermark = img_with_watermark.convert('RGB')
                img_with_watermark.save(output_path, "JPEG", quality=95)
                
                return jsonify({"success": True, "message": "Изображение успешно загружено и обработано"})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)})
    
    return jsonify({"success": False, "error": "No image provided"})

def add_invisible_watermark(img):
    """Добавляет невидимую водяную метку к изображению"""
    # Создаем копию изображения
    watermarked = img.copy()
    
    # Конвертируем в RGBA если нужно
    if watermarked.mode != 'RGBA':
        watermarked = watermarked.convert('RGBA')
    
    # Создаем паттерн водяной метки
    width, height = watermarked.size
    
    # Создаем более заметную водяную метку
    for x in range(0, width, 30):
        for y in range(0, height, 30):
            # Создаем паттерн "ZERO HACKER"
            pattern_x = x // 30
            pattern_y = y // 30
            
            # Создаем паттерн на основе позиции
            if (pattern_x + pattern_y) % 3 == 0:
                # Добавляем едва заметные изменения в пиксели
                for dx in range(3):
                    for dy in range(3):
                        px, py = x + dx, y + dy
                        if px < width and py < height:
                            # Получаем текущий пиксель
                            pixel = watermarked.getpixel((px, py))
                            if len(pixel) == 4:  # RGBA
                                r, g, b, a = pixel
                                # Слегка изменяем зеленый канал
                                g = min(255, g + 5)
                                watermarked.putpixel((px, py), (r, g, b, a))
    
    return watermarked

def generate_encrypted_ip():
    """Генерирует зашифрованный IP адрес"""
    # Простое шифрование: заменяем цифры на буквы
    ip_parts = REAL_IP.split('.')
    encrypted_parts = []
    
    for part in ip_parts:
        encrypted_part = ""
        for char in part:
            if char.isdigit():
                # Заменяем цифры на буквы (A=0, B=1, C=2, etc.)
                encrypted_part += chr(ord('A') + int(char))
            else:
                encrypted_part += char
        encrypted_parts.append(encrypted_part)
    
    return '.'.join(encrypted_parts)


@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("Cache-Control", "no-store")
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
