#!/usr/bin/env python
import docker

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

client = docker.from_env()

@app.route('/manager/worker_completed', methods=['POST'])
def create_job():

    if not request.json or not 'worker_id' in request.json:
        abort(400)

    # print(request.json)

    container = client.containers.get(request.json["worker_id"])

    print(f"Container name is: {container.name}")

    # containers = client.containers.list()

    # for container in containers:
    #     print(container.id)



    return make_response(jsonify({'result': 'success'}), 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'requested resource does not exits'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
