import json
import socket
import threading
import logging
import os
from datetime import datetime

# Настройка логирования
# Директория для логов
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)  # Создаем директорию для логов, если её нет

# Генерируем уникальное имя файла с временной меткой
log_filename = datetime.now().strftime('tcp_server_%Y-%m-%d_%H-%M-%S.log')

# Настройка логирования
logging.basicConfig(
    filename=os.path.join(log_directory, log_filename),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

tcp_client_host = '0.0.0.0'
tcp_client_port = 6000

# Создание сокета и ожидание подключения от клиента
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind((tcp_client_host, tcp_client_port))
tcp_socket.listen(5)

logging.info("TCP Сервер запущен и слушает на порту 6000")


def handle_client(client_socket):
    """
    Обрабатывает подключение клиента.

    Параметры:
        client_socket (socket.socket): Сокет клиента для взаимодействия.
    """
    buffer = ""  # Буфер для хранения данных
    with client_socket:
        while True:
            data = client_socket.recv(1024)
            if not data:
                logging.info("Клиент закрыл соединение.")
                break

            buffer += data.decode('utf-8')

            while True:
                # Попробуем декодировать JSON, если сообщение полное
                try:
                    while buffer:
                        # Пробуем загрузить JSON из буфера
                        data_json = json.loads(buffer)
                        logging.info(f"Получено от клиента: {data_json}")

                        # Очищаем буфер после успешного декодирования
                        buffer = ""

                        # Отправляем ответ
                        response = {"status": "received"}
                        client_socket.sendall(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    # Если ошибка, продолжаем получать данные
                    logging.error("Ошибка декодирования.")
                    break  # Прерываем внутренний цикл, чтобы получить больше данных


def send_request_to_client(data):
    """
    Отправляет запрос клиенту и ожидает ответ.

    Параметры:
        data (dict): Данные для отправки клиенту.

    Возвращает:
        dict: Ответ от клиента.
    """
    client_socket, address = tcp_socket.accept()  # Изменено на tcp_socket
    logging.info(f"Подключен клиент: {address}")

    try:
        # Отправляем запрос клиенту
        logging.info(f"Отправляем данные клиенту: {data}")
        client_socket.sendall(json.dumps(data).encode('utf-8'))

        # Ждем ответа от клиента
        response = client_socket.recv(1024).decode('utf-8')

        # Проверяем и парсим ответ
        if response:
            response_json = json.loads(response)
            logging.info(f"Ответ от клиента: {response_json}")
            return response_json  # Возвращаем весь JSON
        else:
            logging.warning("Получен пустой ответ от клиента.")
            return None

    except json.JSONDecodeError:
        logging.error("Ошибка декодирования JSON.")
        return {"error": "Некорректный ответ от клиента"}
    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        return {"error": str(e)}


# Запуск TCP-сервера в отдельном потоке
def start_tcp_server():
    """
    Запускает TCP-сервер и обрабатывает подключения клиентов.
    """
    while True:
        client_socket, address = tcp_socket.accept()
        logging.info(f"Подключен клиент: {address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()


# Запуск TCP-сервера в основном потоке
if __name__ == "__main__":
    try:
        start_tcp_server()
    except KeyboardInterrupt:
        logging.info("Остановка сервера...")
    finally:
        tcp_socket.close()  # Закрываем сокет сервера при выходе
