# Запуск на сервере (Ubuntu)

Пошаговая инструкция: развернуть и запустить сервис на Ubuntu (с Docker или без).

---

## Вариант 1: Через Docker (рекомендуется)

### 1. Установить Docker и Docker Compose

```bash
# Обновить пакеты
sudo apt update && sudo apt upgrade -y

# Docker
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Проверка
docker --version
docker compose version
```

### 2. Клонировать репозиторий

```bash
cd ~
git clone https://github.com/SpiritWalker84/ML_test.git
cd ML_test
```

### 3. Настроить переменные окружения

```bash
cp .env.example .env
nano .env   # или vi / vim
```

Обязательно заполнить:

- **API_KEY** — ключ OpenAI или прокси (например, api.proxyapi.ru).
- При использовании прокси при необходимости указать **OPENAI_BASE_URL** (например, `https://api.proxyapi.ru/openai/v1`).

Остальное можно оставить по умолчанию (порт 8082 уже задан в `.env.example`).

### 4. Собрать образ и запустить контейнер

```bash
docker compose up --build -d
```

- Образ соберётся (в т.ч. обучение ML-модели).
- Приложение будет слушать порт **8082** на всех интерфейсах.

### 5. Проверить работу

```bash
curl -s http://localhost:8082/ | head -5
```

В браузере: `http://<IP_сервера>:8082`.

### 6. Полезные команды

```bash
# Логи
docker compose logs -f app

# Остановить
docker compose down

# Перезапустить (после изменения .env)
docker compose down && docker compose up -d
```

---

## Вариант 2: Без Docker (Python на хосте)

### 1. Установить Python 3.10+ и зависимости

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git
cd ~
git clone https://github.com/SpiritWalker84/ML_test.git
cd ML_test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Настроить .env

```bash
cp .env.example .env
nano .env
```

Заполнить **API_KEY** (и при необходимости **OPENAI_BASE_URL**). Порт по умолчанию — 8082 (`PORT=8082`).

### 3. Обучить модель (один раз)

```bash
source venv/bin/activate
python scripts/train_model.py
```

### 4. Запустить приложение

**Обычный запуск (в текущем терминале):**

```bash
source venv/bin/activate
python run.py
```

Сервис будет доступен на `http://0.0.0.0:8082`.

**Запуск в фоне (nohup):**

```bash
source venv/bin/activate
nohup python run.py > app.log 2>&1 &
```

**Через systemd (автозапуск при перезагрузке):**

Создать файл:

```bash
sudo nano /etc/systemd/system/ml-test.service
```

Содержимое (подставьте свой путь и пользователя):

```ini
[Unit]
Description=ML_test debt AI service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ML_test
Environment="PATH=/home/ubuntu/ML_test/venv/bin"
ExecStart=/home/ubuntu/ML_test/venv/bin/python run.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Включить и запустить:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ml-test
sudo systemctl start ml-test
sudo systemctl status ml-test
```

Логи: `journalctl -u ml-test -f`.

### 5. Открыть порт в файрволе (если включён ufw)

```bash
sudo ufw allow 8082/tcp
sudo ufw reload
```

---

## Краткая шпаргалка (Docker на Ubuntu)

| Действие              | Команда |
|-----------------------|--------|
| Клонировать            | `git clone https://github.com/SpiritWalker84/ML_test.git && cd ML_test` |
| Настроить .env         | `cp .env.example .env` и заполнить `API_KEY` |
| Запустить              | `docker compose up --build -d` |
| Открыть в браузере     | `http://<IP>:8082` |
| Логи                   | `docker compose logs -f app` |
| Остановить             | `docker compose down` |

Репозиторий: [https://github.com/SpiritWalker84/ML_test](https://github.com/SpiritWalker84/ML_test).
