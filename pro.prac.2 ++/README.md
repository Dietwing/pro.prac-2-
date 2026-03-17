# Проектный практикум. Задание 2 + подготовка к заданию 8

Данный репозиторий содержит работоспособное приложение аналитики по проекту **«НРИ-Помощник (офлайн)»**, созданное в рамках второго задания по проектному практикуму и дополненное материалами, полезными для итогового восьмого задания.

## Структура проекта
- `nri_combat_analytics_dashboard/app.py` — основное приложение Dash;
- `nri_combat_analytics_dashboard/assets/style.css` — стили оформления;
- `nri_combat_analytics_dashboard/data/*.csv` — тестовый набор игровых данных;
- `tests/` — файлы для тестирования интерфейса и нагрузки;
- `security/` — инструкции по проведению анализа безопасности;
- `Dockerfile` — описание контейнерной сборки.

## Запуск приложения
```bash
cd nri_combat_analytics_dashboard
pip install -r requirements.txt
python app.py
```

После запуска приложение будет доступно по адресу `http://127.0.0.1:8050`.

## Запуск pytest
Из корня репозитория:
```bash
pip install -r requirements-dev.txt
pytest tests/test_ui_pytest.py -v
```

## Запуск Playwright
```bash
pip install -r requirements-dev.txt
playwright install chromium
pytest tests/test_ui_playwright.py -v
```

## Нагрузочное тестирование
```bash
pip install -r requirements-dev.txt
locust -f tests/locustfile.py --host=http://127.0.0.1:8050
```

## Анализ безопасности Trivy
Инструкции находятся в файле `security/trivy_instructions.md`.

## Docker-сборка
```bash
docker build -t nri-combat-analytics .
docker run -p 8050:8050 nri-combat-analytics
```


## Примечание по Playwright
В средах наподобие GitHub Codespaces браузерный тест может быть автоматически пропущен, если в системе отсутствуют низкоуровневые зависимости Chromium. Это не влияет на запуск pytest-проверок HTTP и layout-части приложения.
