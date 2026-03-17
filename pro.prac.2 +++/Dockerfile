FROM python:3.11-slim

WORKDIR /app

COPY nri_combat_analytics_dashboard/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY nri_combat_analytics_dashboard ./nri_combat_analytics_dashboard

WORKDIR /app/nri_combat_analytics_dashboard
EXPOSE 8050

CMD ["python", "app.py"]
