webhook-glpi
==============

*Validação de cache Docker otimizado*

.. image:: https://img.shields.io/badge/python-3.10-blue.svg
    :target: https://pypi.org/project/webhook-exporter/

.. image:: https://travis-ci.org/MyBook/webhook-exporter.svg?branch=master
    :target: https://travis-ci.org/MyBook/webhook-exporter

.. image:: https://codecov.io/gh/MyBook/webhook-exporter/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/MyBook/webhook-exporter

Usage
=====
::

    Usage: webhook-glpi [OPTIONS]

      webhook metrics exporter for Prometheus.

      Use the config file to map webhook metrics names/labels into Prometheus. For example:

          webhook.metric[device,uptime] = 86400
          webhook.metric[device,last_contacted] = 1634857850

      Transforms into Prometheus format:

          webhook_device_uptime{device="ap01"} 86400
          webhook_device_last_contacted{device="ap01"} 1634857850

      YAML Example:

          metrics:
            - key: 'webhook.metric[device,*]'
              name: 'webhook_device_metric'
              labels:
                metric: $1

    Options:
      --config PATH               Path to exporter config file
      --port INTEGER              Port to serve Prometheus metrics [default: 9224]
      --url TEXT                  webhook AirWave API URL
      --token TEXT             webhook AirWave token
      --verify-tls / --no-verify  Enable TLS certificate verification [default: true]
      --timeout INTEGER           API read/connect timeout
      --verbose                   Enable verbose output
      --version                   Show version information
      --help                      Show this message and exit.

Deploying with Docker
=====================
::

    docker run -d --name webhook-glpi \
    -v /path/to/your/config.yml:/app/webhook-glpi/webhook-glpi.yml \
    --env=DISCORD_WEBHOOK= \
    --env="API_HOST_GLPI=secret" \
    --env="API_USER_TOKEN=secret" \
    --env="API_TOKEN=secret"
    mybook/webhook-glpi
