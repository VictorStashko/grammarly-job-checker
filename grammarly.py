import requests
from bs4 import BeautifulSoup
import json
import os
import time

# === Налаштування ===
URL = "https://www.grammarly.com/careers/jobs#engineering:all"
QA_KEYWORDS = ["QA", "Quality Assurance", "Test Engineer", "Automation Engineer", "Software Tester", "SDET", "Software Engineer, Front-End"]
TELEGRAM_BOT_TOKEN = "7554001792:AAGOPajMtn6XxJzxmidA3XZOU-ZCK5JVc5k"  # Встав свій токен
TELEGRAM_CHAT_ID = "439949640"  # Встав свій ID
DATA_FILE = "vacancies.json"


def fetch_vacancies():
    """Отримує вакансії з сайту"""
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("Помилка завантаження сторінки:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    # Знаходимо всі вакансії
    for job in soup.find_all("h3"):  # Приблизна структура, потрібно перевірити
        title = job.text.strip()
        if any(keyword in title for keyword in QA_KEYWORDS):
            jobs.append(title)

    return jobs


def load_previous_vacancies():
    """Завантажує попередні вакансії, якщо є"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_vacancies(vacancies):
    """Зберігає вакансії у файл"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(vacancies, file, ensure_ascii=False, indent=2)


def send_telegram_message(message):
    """Відправляє повідомлення в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)


def main():
    print("🔍 Перевіряємо вакансії...")
    current_vacancies = fetch_vacancies()
    previous_vacancies = load_previous_vacancies()

    new_vacancies = [job for job in current_vacancies if job not in previous_vacancies]

    if new_vacancies:
        print(f"✅ Знайдено нові вакансії: {len(new_vacancies)}")
        message = "📢 Нові вакансії в Grammarly:\n\n" + "\n".join(f"- {job}" for job in new_vacancies)
        send_telegram_message(message)
        save_vacancies(current_vacancies)
    else:
        print("❌ Нових вакансій немає.")


if __name__ == "__main__":
    main()

