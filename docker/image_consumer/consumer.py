import pika
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

UPLOAD_FOLDER = '/data/images'
MAX_RETRIES = 5
RETRY_DELAY = 5

def callback(ch, method, properties, body):
    filename = body.decode()
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        animal_type = 'unknown'
        name_without_id_ext = os.path.splitext(filename)[0].split("_", 1)[1]
        if 'cat' in name_without_id_ext.lower():
            animal_type = 'cat'
        elif 'dog' in name_without_id_ext.lower():
            animal_type = 'dog'

        logging.info(f'Image {filename} contains a {animal_type}. Size: {file_size} bytes.')
    else:
        logging.warning(f'Image with filename {filename} not found.')

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connected = False
    retry_delay = RETRY_DELAY

    for attempt in range(MAX_RETRIES):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)
            channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=False)
            connected = True
            logging.info('Consumer is waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as error:
            logging.error(f'Connection failed: {error}. Retrying in {retry_delay} seconds.')
            time.sleep(retry_delay)
            retry_delay *= 2  
        except Exception as e:
            logging.exception("An unexpected error occurred.", e)
            break

        if connected:
            break
    else:
        logging.error('Could not connect to RabbitMQ after several attempts.')

if __name__ == '__main__':
    main()
