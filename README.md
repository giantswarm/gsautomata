# GS Automata

Hackathon project that will try to remediate issues on Tenant clusters when an alarm is in Pending on Prometheus.

This project has two components:

## AlertBridge

### What does it do?
- Scrape Prometheus alert endpoint searching for alerts in Pending state and launch a Kubernetes Job.
    - It will scrape Prometheus every 10 seconds.
    - It will store executions internally for 1 hour in order to avoid launching multiple jobs for the same alarm.
    - It will only fire a job if it's whitelisted.
    - It will only fire a job that is in Pending for more than 15 seconds.
- Provides a web interface to show previous jobs and logs.
    - Jobs are configured to be deleted from kubernetes after 1 hour.

## GSAutomata

### What does it do?
- Executes a generic script against the Control Plane API to gather tenant cluster information.
- Executes a script to generate a Tenant Cluster kubeconfig from a secret.
- Executes a script against the Tenant Cluster to gather common data.
- Executes a script against the Tenant Cluster specific to the fired alarm.
- All the labels of the alarm will be present during the execution as environment variables.


## Future ideas
- Store debugging scripts on ops-recipes.
- Enable connectivity to cloud providers.
- Allow filtering alarms per Tenant Cluster version.
- Send report to Slack/S3...
