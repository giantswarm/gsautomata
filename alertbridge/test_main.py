import json
from flask import Flask

from background import alertMD5, fireAutomation, filterAlerts, cleanOldAlerts

app = Flask(__name__)

json_response = """
    {
        "status": "success",
        "data": {
            "alerts": [
            {
                "labels": {
                    "alertname": "ChartOrphanSecret",
                    "app": "chart-operator",
                    "area": "managedservices",
                    "cluster_id": "u8gjs",
                    "cluster_type": "guest",
                    "exported_namespace": "giantswarm",
                    "instance": "master.u8gjs:443",
                    "job": "guest-cluster-u8gjs-workload",
                    "namespace": "giantswarm",
                    "node": "ip-172-19-67-43.eu-west-1.compute.internal",
                    "pod_name": "chart-operator-f5c55f579-82tbc",
                    "provider": "aws",
                    "severity": "notify",
                    "team": "batman",
                    "topic": "releng"
                },
                "annotations": {
                    "description": "Chart secrets have not been deleted.",
                    "opsrecipe": "chart-orphan-resources/"
                },
                "state": "pending",
                "activeAt": "2020-12-14T11:11:15.611214297Z",
                "value": "1e+00"
            },
            {
                "labels": {
                    "alertname": "InhibitionClusterStatusCreated",
                    "app": "cluster-operator",
                    "app_instance": "cluster-operator-3.4.1",
                    "app_name": "cluster-operator",
                    "app_version": "3.4.1",
                    "area": "kaas",
                    "cluster_id": "u8gjs",
                    "cluster_status_created": "true",
                    "cluster_type": "host",
                    "exported_cluster_id": "u8gjs",
                    "instance": "100.64.45.94:8000",
                    "job": "host-cluster-ginger-workload",
                    "namespace": "giantswarm",
                    "node": "ip-10-0-5-19.eu-west-1.compute.internal",
                    "pod_phase": "Running",
                    "pod_ready": "true",
                    "provider": "aws",
                    "release_version": "13.0.0",
                    "status": "Created",
                    "team": "ludacris",
                    "topic": "status"
                },
                "annotations": {
                    "description": "Cluster u8gjs has status condition 'Created'."
                },
                "state": "firing",
                "activeAt": "2020-12-14T11:08:11.483808611Z",
                "value": "1e+00"
            }
            ]
        }
    }
    """


def setUp(self):
    self.app_context = app.app_context()
    self.app_context.push()

def tearDown(self):
    self.app_context.pop()

def test_parse():
    alerts = json.loads(json_response)
    assert len(alerts["data"]["alerts"])==2

def test_filter():
    alerts = json.loads(json_response)
    assert len(filterAlerts(alerts["data"]["alerts"], "pending"))==1

def test_md5():
    alerts = json.loads(json_response)
    alertMD5(alerts["data"]["alerts"][0])

    assert len(alerts["data"]["alerts"])==2

def test_clean():
    alerts = json.loads(json_response)

    firedAlerts = {}
    for alert in alerts["data"]["alerts"]:
        firedAlerts[alertMD5(alert)] = alert

    currentAlerts = cleanOldAlerts(firedAlerts)

    assert len(currentAlerts)==0

def test_fired():
    alerts = json.loads(json_response)

    with app.test_request_context(""):
        fired = fireAutomation(alerts["data"]["alerts"][0])
        assert fired==True
        fired = fireAutomation(alerts["data"]["alerts"][1])
        assert fired==True

        fired = fireAutomation(alerts["data"]["alerts"][0])
        assert fired==False
        fired = fireAutomation(alerts["data"]["alerts"][1])
        assert fired==False
