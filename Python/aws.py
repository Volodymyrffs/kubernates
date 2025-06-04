import boto3
import logging
import os
import requests
import time
from datetime import datetime

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Замініть на свій регіон AWS
region_name = 'eu-central-1'
client = boto3.client('rekognition', region_name=region_name)

# Отримання токена бота та ID чату з змінних середовища
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_photo(bot_token, chat_id, photo_path, caption):
    """Відправляє фотографію з підписом у Telegram."""
    if not bot_token or not chat_id:
        logging.warning("Токен Telegram-бота або ID чату не налаштовано.")
        return

    send_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    files = {'photo': open(photo_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': caption}
    try:
        response = requests.post(send_url, files=files, data=data)
        response.raise_for_status()
        logging.info(f"Фото до Telegram успішно відправлено з підписом: '{caption}'")
    except requests.exceptions.RequestException as e:
        logging.error(f"Помилка відправлення фото до Telegram: {e}")

def compare_faces(source_image_path, target_image_path, similarity_threshold=70):
    """Порівнює обличчя на двох локальних зображеннях."""
    try:
        with open(source_image_path, 'rb') as source_image:
            source_bytes = source_image.read()
        with open(target_image_path, 'rb') as target_image:
            target_bytes = target_image.read()

        response = client.compare_faces(
            SourceImage={'Bytes': source_bytes},
            TargetImage={'Bytes': target_bytes},
            SimilarityThreshold=similarity_threshold
        )
        return response
    except Exception as e:
        logging.error(f"Помилка порівняння облич: {e}")
        return None

def get_file_creation_time(file_path):
    """Отримує час створення файлу як об'єкт datetime."""
    timestamp = os.path.getctime(file_path)
    return datetime.fromtimestamp(timestamp)

if __name__ == '__main__':
    source_image_file = 'directory/original/obama.jpg'
    target_directory = 'directory/source/'

    while True:
        try:
            target_files = [os.path.join(target_directory, f) for f in os.listdir(target_directory) if os.path.isfile(os.path.join(target_directory, f))]
            if not target_files:
                logging.info(f"Не знайдено файлів у директорії: {target_directory}. Очікування...")
                time.sleep(60)
                continue

            # Сортування файлів за часом створення (найстаріші перші)
            target_files.sort(key=get_file_creation_time)

            for target_image_file in target_files:
                telegram_photo_path = target_image_file
                logging.info(f"Обробка файлу: {target_image_file}")

                comparison_result = compare_faces(source_image_file, target_image_file)

                if comparison_result:
                    if 'FaceMatches' in comparison_result and comparison_result['FaceMatches']:
                        similarity = comparison_result['FaceMatches'][0]['Similarity']
                        logging.info(f"Знайдено відповідність обличчя зі схожістю: {similarity}%")
                        message = f"Ідентифіковано людину зі схожістю {similarity:.2f}%."
                        send_telegram_photo(BOT_TOKEN, CHAT_ID, telegram_photo_path, message)
                    else:
                        logging.info("Облич не знайдено або не знайдено достатньо схожих відповідностей.")
                else:
                    logging.warning("Результат порівняння облич відсутній.")

                # Видалення обробленого цільового фото
                try:
                    os.remove(target_image_file)
                    logging.info(f"Видалено оброблений файл: {target_image_file}")
                except FileNotFoundError:
                    logging.warning(f"Не вдалося знайти файл для видалення: {target_image_file}")
                except Exception as e:
                    logging.error(f"Помилка при видаленні файлу: {e}")

            time.sleep(7) # Затримка між перевірками на нові файли
        except Exception as e:
            logging.error(f"Загальна помилка в головному циклі: {e}")
            time.sleep(60)
