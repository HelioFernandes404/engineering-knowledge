from sf_common.metrics.metric import MetricManager

app_name = "webhook_glpi"
metric_manager = MetricManager(app_name)

sf_id_lookup_failed_counter = metric_manager.create_counter(
    "sf_id_lookup_failed", "Counter for failed SF ID", "1"
)

request_dynamodb_counter = metric_manager.create_counter(
    "request_dynamodb", "Counter for request to DynamoDB", "1"
)

glpi_problem_created = metric_manager.create_counter(
    "glpi_problem_created", "Counter for notification", "1"
)

notification_received_counter = metric_manager.create_counter(
    "notification_received", "Counter for notification received", "1"
)
post_discord_counter = metric_manager.create_counter(
    "post_discord", "Counter for posting to Discord", "1"
)
post_failed_discord_counter = metric_manager.create_counter(
    "post_failed_discord", "Counter for failed posting to Discord", "1"
)
resolved_problem_counter = metric_manager.create_counter(
    "resolved_problem", "Counter for resolved problem", "1"
)
glpi_exception_counter = metric_manager.create_counter(
    "glpi_exception", "Counter for GLPI exception", "1"
)

item_equipment_failed_counter = metric_manager.create_counter(
    "item_equipment_failed", "Counter for failed item equipment", "1"
)

app_started_counter = metric_manager.create_counter(
    "app_started", "Incremet when metric is started", "1"
)
app_stopped_counter = metric_manager.create_counter(
    "app_stopped", "Incremet when metric is stopped", "1"
)
