## Проверка файловой системы проекта
```bash
trivy fs .
```

## Проверка Docker-образа
Сначала собрать образ:
```bash
docker build -t nri-combat-analytics .
```

Затем выполнить сканирование:
```bash
trivy image nri-combat-analytics
```
