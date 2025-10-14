# Zero Hacker — Matrix Flask мини-игра

Мини-режим: один экран `/run` с тремя шагами и финал `/end`.

## Локальный запуск (Windows / PowerShell)
```powershell
cd C:\projects\zero_hacker
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY="matrix-green"
python app.py
```
Открой: `http://127.0.0.1:5000/`

## Docker
Сборка и запуск:
```bash
docker compose up --build -d
# затем открой
# http://localhost:8000
```
Остановить:
```bash
docker compose down
```
Переменные окружения:
- SECRET_KEY — секрет Flask (по умолчанию `matrix-green`)
- PORT — внутренний порт приложения (в Docker 8000)

## Маршруты
- `/` — стартовый экран (Старт)
- `/run` — три шага (ПИНГ ×3 → ключ `1111` → слайдер в зелёную зону)
- `/end` — финальная сцена и ссылка на `http://138.124.81.201/`

## Зависимости
См. `requirements.txt` (Flask + Gunicorn для продакшена). `waitress` убран — запускаемся через Gunicorn в Docker.
