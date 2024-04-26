from flask import Flask, request, jsonify
import pika
import uuid
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/data/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    original_name = file.filename
    correlation_id = str(uuid.uuid4())
    file_extension = os.path.splitext(original_name)[1]
    saved_filename = f"{correlation_id}_{original_name}"
    file_path = os.path.join(UPLOAD_FOLDER, saved_filename)
    file.save(file_path)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=saved_filename,
        properties=pika.BasicProperties(
            delivery_mode=2,  
        )
    )
    connection.close()

    return jsonify({'correlation_id': correlation_id, 'filename': saved_filename})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
