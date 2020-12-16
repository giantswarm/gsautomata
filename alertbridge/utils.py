import hashlib
import json

# Remove changing values to recalculate md5 of an alert
def alertMD5(alert):
    if "value" in alert:
        del alert["value"]
    return hashlib.md5(json.dumps(alert).encode('utf-8')).hexdigest()
