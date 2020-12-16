import pykube
import json
import base64

from utils import alertMD5

def getEnvVars(alert):
    env = []
    for key in alert["labels"]:
        env.append({
            "name": key.upper(),
            "value": alert["labels"][key]
        })
    return env

def createJob(alert):
    api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

    md5alert = alertMD5(alert)

    try:
        job = pykube.Job.objects(api).get(namespace="giantswarm", name=md5alert)
        return md5alert
    except pykube.exceptions.ObjectDoesNotExist:
        pass

    env_vars = getEnvVars(alert)

    obj = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": md5alert,
            "namespace": "giantswarm",
            "labels": {
                "app": "gsautomata",
            },
            "annotations": {
                "alert-base64": base64.b64encode(json.dumps(alert).encode('ascii')).decode("utf-8"),
            }
        },
        "backoffLimit": 4,
        "spec": {
            "ttlSecondsAfterFinished": 3600,
            "template": {
                "spec": {
                    "serviceAccountName": "gsautomata-jobs",
                    "containers": [
                        {
                            "name": "gsautomata",
                            "image": "paurosello/gsautomata:0.0.14",
                            "env": env_vars
                        }
                    ],
                    "restartPolicy": "OnFailure"
                }
            }
        }
    }

    pykube.Job(api, obj).create()

    return md5alert
