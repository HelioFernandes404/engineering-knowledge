[
    {
        "id": "1177613",
        "name": "BR Properties - PDC",
        "url": "https://n406.meraki.com/o/jsnXhd/manage/organization/overview",
        "api": {"enabled": True},
        "licensing": {"model": "per-device"},
        "cloud": {
            "region": {"name": "North America", "host": {"name": "United States"}}
        },
        "management": {
            "details": [
                {"name": "customer number", "value": "44015362"},
                {"name": "IP restriction mode for API", "value": "client allowed"},
            ]
        },
    }
]


class Organization(object):
    _id: str
    name: str
    url: str
    api_enabled: bool
    licensing_model: str
    cloud_region: dict
    management_details: dict
