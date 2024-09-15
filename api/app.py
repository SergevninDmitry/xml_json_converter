import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from worker import celery
import os

basedir = os.path.abspath(os.path.dirname(__file__))

flask_app = Flask(__name__)
flask_app.config.from_object("config.Config")


@flask_app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@flask_app.route('/application/json', methods=['POST'])
def start_chair_from_json_to_xml() -> Response:
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        data = {
            'data': json_data,
            'format': 'json'
        }
        task = celery.send_task('tasks.run_chair', args=[data], kwargs={})
        response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id}</a>"
        return jsonify({'message': response}), 202
    return jsonify('Please, using POST request'), 405


@flask_app.route('/application/xml', methods=['POST'])
def start_chair_from_xml_to_json() -> Response:
    if request.method == 'POST':
        xml_file = request.data.decode('utf-8')
        data = {
            'data': xml_file,
            'format': 'xml'
        }
        print(data)
        task = celery.send_task('tasks.run_chair', args=[data], kwargs={})
        response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id}</a>"
        return jsonify({'message': response}), 202
    return jsonify('Please, using POST request'), 405


@flask_app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5001, debug=True)
