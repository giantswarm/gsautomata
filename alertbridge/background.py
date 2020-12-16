import os
import json
from datetime import datetime

from flask import current_app
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from automation import createJob
from utils import alertMD5

# Prometheus scraping URL
PROMETHEUSURL = os.getenv('PROMETHEUSURL', "http://prometheus.monitoring.svc.cluster.local:9090")
# Ignore alerts not present in this list
MANAGEDALERTS = [
    "CoreDNSDeploymentNotSatisfied",
    "KiamMetadataFindRoleErrors",
    "TenantClusterManagedDeploymentNotSatisfied"
]
# Remove alerts from internal cache in seconds
CLEANALERTSAFTER = 3600
# Automation will be fired afeter this period in seconds
ALERTMINLIFE = 15

firedAlerts = {}

# Filter alerts by status, not doable on the API level
def filterAlerts(alerts, status):
    filtered_status = list(filter(lambda x: x.get('state', "") == status, alerts))
    filtered_alerts = list(filter(lambda x: x['labels']['alertname'] in MANAGEDALERTS, filtered_status))
    return filtered_alerts
# Fire alerts only if they are in "Pending" for 60 seconds to avoid quick flaps
def checkAutomationFired(alert):
    md5alert = alertMD5(alert)
    return md5alert in firedAlerts.keys()

# Fire alerts only if they are in "Pending" for 15 seconds to avoid quick flaps
def checkAlertShouldFire(alert):
    current_time = datetime.now()
    alert_time = parseDate(alert["activeAt"])
    diff_time = current_time - alert_time

    return diff_time.seconds > ALERTMINLIFE

# Try to fire automation for an alert. Will check if it has not been fired and has been in pending for 60 seconds.
def fireAutomation(alert):
    alert_name = alert["labels"]["alertname"]
    if checkAutomationFired(alert)==False:
        if checkAlertShouldFire(alert) == False:
            current_app.logger.debug(f'Waiting for alert {alert_name} to be older than 60 seconds')
            return False
        else:
            alertmd5 = createJob(alert)
            current_app.logger.info(f'Firing automation for {alertmd5} alert {alert_name}')
            firedAlerts[alertmd5] = alert
            return True
    else:
        current_app.logger.debug(f'Skiping automation for alert {alert_name}')
        return False

# Retrieve alarms from prometheus and try to fire automation.
def scrapePrometheus(server):
    with server.app_context():
        full_url = PROMETHEUSURL+"/api/v1/alerts"
        server.logger.debug(f'Scraping Prometheus alarms from {full_url}.')
        alerts_request = requests.get(full_url)
        alerts=alerts_request.json()["data"]["alerts"]
        pending_alerts = filterAlerts(alerts, "pending")
        pending_alerts_len = len(pending_alerts)
        server.logger.debug(f'Found {pending_alerts_len} alerts in Pending state.')

        for alert in pending_alerts:
            fireAutomation(alert)
    return

# Remove microseconds from date returned from Prometheus as the format is not consistent on the API
def parseDate(date):
    cut_micro = date.split(".")[0]
    return datetime.strptime(cut_micro, '%Y-%m-%dT%H:%M:%S')

# Clean alarms older than 1 hour
def cleanOldAlerts(alerts):
    for key in list(alerts.keys()):
        alert = alerts[key]
        current_time = datetime.now()
        alert_time = parseDate(alert["activeAt"])
        diff_time = current_time - alert_time

        if diff_time.total_seconds() > CLEANALERTSAFTER:
            del alerts[key]

    return alerts

def cleanCachedAlerts(firedAlerts):
    firedAlerts = cleanOldAlerts(firedAlerts)

def setupScheduler(server):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: scrapePrometheus(server), 'interval', seconds=10)
    scheduler.add_job(lambda: cleanCachedAlerts(firedAlerts), 'interval', seconds=900)
    scheduler.start()
