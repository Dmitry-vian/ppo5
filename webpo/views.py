import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tcp_server import send_request_to_client
import os
from datetime import datetime

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

@csrf_exempt
def send_to_client(request):
    """
    Обрабатывает запросы от веб-клиента и отправляет их клиенту по TCP.

    Args:
        request (HttpRequest): HTTP-запрос от веб-клиента.

    Returns:
        JsonResponse: Ответ в формате JSON.
            - Если метод POST: JSON с результатами обработки запроса.
            - Если метод GET: JSON с данными для packetType 3 или 20.
            - Если метод не поддерживается: сообщение об ошибке.
    """
    if request.method == 'POST':
        try:
            # Получаем данные из HTTP-запроса
            data = json.loads(request.body)
            logging.info(f"Получен запрос от веб-клиента: {json.dumps(data, indent=4)}")

            # Определяем packetType
            packet_type = data.get("packetType")

            # Отправляем запрос клиенту по TCP
            response_from_client = send_request_to_client(data)
            if not response_from_client:
                logging.error("Нет ответа от клиента")
                return JsonResponse({"error": "Нет ответа от клиента"}, status=500)

            # Используем готовую функцию для генерации ответа
            return JsonResponse(generate_response(packet_type, response_from_client))

        except json.JSONDecodeError:
            logging.error("Некорректный JSON")
            return JsonResponse({"error": "Некорректный JSON"}, status=400)

    elif request.method == 'GET':
        # Обрабатываем GET запрос только для packetType 3 и 20
        packet_type = request.GET.get("packetType")  # Получаем packetType из параметров URL
        if packet_type in ['3', '20']:  # Проверяем, что packetType 3 или 20
            data = {
                "packetType": int(packet_type)
            }
            response_from_client = send_request_to_client(data)
            if not response_from_client:
                logging.error("Нет ответа от клиента")
                return JsonResponse({"error": "Нет ответа от клиента"}, status=500)

            logging.info(f"Успешно обработан запрос для packetType {packet_type}.")
            return JsonResponse({"status": "success", "data": response_from_client})

        logging.warning("packetType должен быть 3 или 20")
        return JsonResponse({"error": "packetType должен быть 3 или 20"}, status=400)

    logging.warning("Метод не поддерживается")
    return JsonResponse({"error": "Метод не поддерживается"}, status=405)


def generate_response(packet_type, response_from_client):
    """
    Генерирует ответ на основе packetType.

    Args:
        packet_type (int): Тип пакета (packetType).
        response_from_client (any): Ответ от клиента.

    Returns:
        dict: Словарь с ответом, содержащий статус, данные и сообщение.
    """
    return {
        "status": "success",
        "data": response_from_client,
        "message": f"Успешно обработан запрос для packetType {packet_type}."
    }
