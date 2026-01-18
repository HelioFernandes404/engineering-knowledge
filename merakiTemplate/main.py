from pprint import pp
import meraki
from client.meraki_client import MerakiClient
from config.env_config import EnvConfig

env = EnvConfig()
dashboard: meraki.DashboardAPI = meraki.DashboardAPI(
    env.get_api_key(), output_log=False, print_console=False
)

client = MerakiClient(dashboard)
