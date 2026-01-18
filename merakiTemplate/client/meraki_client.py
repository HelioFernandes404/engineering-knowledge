from loguru import logger
import meraki


class MerakiClient:
    def __init__(self, dashboard_api):
        self.client: meraki.DashboardAPI = dashboard_api

    logger.catch(
        reraise=True,
        message="An error occurred while trying to get organizations",
    )

    def get_organizations(self):
        return self.client.organizations.getOrganizations()

    logger.catch(
        reraise=True,
        message="An error occurred while trying to get organization ID",
    )

    def get_organizationId(self) -> str:
        return self.client.organizations.getOrganizations()[0]["id"]

    def get_organization_devices(self):
        return self.client.organizations.getOrganizationDevices(
            self.get_organizationId(), total_pages="all"
        )
