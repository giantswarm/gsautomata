import json
import base64

from flask import Flask, jsonify, render_template, current_app
import logging
import pykube

import pykubecustom
import background

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
background.setupScheduler(app)

@app.route('/')
def index():
    api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())
    jobs = pykube.Job.objects(api).filter(namespace="giantswarm", selector={"app": "gsautomata"})
    automations = []
    for job in jobs:
        object_str = base64.decodebytes(job.annotations["alert-base64"].encode("utf-8"))
        object_json = json.loads(object_str)
        object_json["job_name"] = job.name
        automations.append(object_json)

    return render_template('index.html', automations=automations)

@app.route('/automationdetails/<automationid>')
def automationdetails(automationid):
    api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

    job = pykube.Job.objects(api).get(namespace="giantswarm", name=automationid)
    automation_str = base64.decodebytes(job.annotations["alert-base64"].encode("utf-8"))
    automation_json = json.loads(automation_str)

    pods = pykube.Pod.objects(api).filter(namespace="giantswarm", selector={"job-name": automationid})

    logs=[]
    for pod in pods:
        pod_obj = pykube.Pod.objects(api).get(namespace="giantswarm", name=pod)
        logs.append(pod_obj.logs(pretty=True).strip())

    return render_template('automationdetails.html', automation=automation_json, logs=logs)

@app.route('/cachedalerts')
def cachedalerts():
    return jsonify(background.firedAlerts)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=5000, use_reloader=False)
