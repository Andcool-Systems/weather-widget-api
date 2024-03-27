# Устанавливаем официальный образ Python в качестве базового образа
FROM python:latest

# Устанавливаем переменную среды PYTHONUNBUFFERED для вывода вывода stdout/stderr в реальном времени без буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем директорию приложения в контейнере
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

# Указываем команду для запуска вашего приложения
CMD ["python3", "index.py"]