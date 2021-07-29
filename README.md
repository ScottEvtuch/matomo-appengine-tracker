
# Matomo Tracking for AppEngine Logs #

This repo contains a Python script intended to be used as a [Google Cloud Function](https://cloud.google.com/functions) for log-based tracking of a site hosted in [Google App Engine](https://cloud.google.com/appengine). The functionality should be similar to using Matomo's [log analytics tool](https://matomo.org/docs/log-analytics-tool-how-to/) on a traditional site hosted on an Apache server, for example.

## Usage ##

### Configuration ###

The only required configuration is to update the config.json with your Matomo information:

```
"MATOMO_URL": "https://analytics.example.com/matomo.php",
"AUTH_TOKEN": "your_api_key",
"SITE_ID": 0,
```

### Cloud Build ###

A cloudbuild.yaml file is included that will set up all of the required Google Cloud Platform configuration. All that is required is to grant the Cloud Build service account the following IAM roles:

* Cloud Build Service Account
* Cloud Functions Developer
* Service Account User
* Logs Configuration Writer
* Pub/Sub Admin
