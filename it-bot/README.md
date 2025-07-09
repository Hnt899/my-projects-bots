# BaseBot TEMPLATE

![Basebot](./img/baner.jpg)

> [!IMPORTANT]
> Должен быть установлен Python3.11 и python3.11-venv

> [Установка Python3.11](https://zomro.com/rus/blog/faq/473-installing-python-311-on-ubuntu-2204)

## Конфигурация
- Создайте `src/config/config.ini` как `src/config/config.ini.example`, предварительно создав токен бота в Botfather.
- Эта версия проекта работает с SQLite

## Как запустить локально
1. Установите всё, что нужно командой `make install`
2. Запустите `make`
## Как развернуть на сервере linux

1. Создайте следующий файл на сервере `basebot_bot.service` и поместите `/etc/stystemd/system/`

```bash
[Service]
WorkingDirectory=path/to/project/src
User=root
ExecStart=path/to/project/.venv/bin/python3.11 main.py
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target

```

> [!TIP] 
> Воспользуйтесь командой `make install` и пропустите шаги 2-3

2. Перейдите в проект установите venv python>3.11 и зависимости + запустите alembic

```bash
python3.11 -m venv .venv
source ./venv/bin/activate
pip install -r requirements.txt
cd ./src
alembic revision --autogenerate -m 'init'
alembic upgrade head
```

3. Установите Redis

```bash
sudo apt update && sudo apt upgrade
sudo apt install redis
redis-cli --version
```

4. Запустите проект:

```bash
systemctl start basebot_bot.service
systemctl status basebot_bot.service
```

5. Останновить

```bash
systemctl stop logist_bot.service
```

6. Деинсталировать

```bash
make uninstall
```

# basebot_template
