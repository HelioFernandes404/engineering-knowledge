# -*- coding: utf-8 -*-
"""GLPI API client with session management."""
import requests
from typing import Optional, Dict, Any, List
from .config import Config
from .errors import GLPIError, raise_glpi_error


class GLPIClient:
    """Client for GLPI REST API with automatic session management."""

    def __init__(self, config: Config):
        """Initialize GLPI client.

        Args:
            config: Configuration with URL and tokens
        """
        self.config = config
        self.session_token: Optional[str] = None
        self.base_url = config.url.rstrip("/")

    def _get_headers(self, include_session: bool = False) -> Dict[str, str]:
        """Build request headers.

        Args:
            include_session: Whether to include Session-Token header

        Returns:
            Dictionary of headers
        """
        headers = {
            "Content-Type": "application/json",
            "App-Token": self.config.app_token,
        }

        if include_session and self.session_token:
            headers["Session-Token"] = self.session_token

        return headers

    def init_session(self):
        """Initialize GLPI session and store session token.

        Raises:
            GLPIError: If session initialization fails
        """
        url = f"{self.base_url}/initSession"
        headers = {
            "Content-Type": "application/json",
            "App-Token": self.config.app_token,
            "Authorization": f"user_token {self.config.user_token}",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get("session_token")
                if not self.session_token:
                    raise GLPIError("Session token n\u00e3o retornado pela API")
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def kill_session(self):
        """Kill current GLPI session.

        Raises:
            GLPIError: If session termination fails
        """
        if not self.session_token:
            return

        url = f"{self.base_url}/killSession"
        headers = self._get_headers(include_session=True)

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            # Don't fail hard on session kill errors
            pass
        finally:
            self.session_token = None

    def get_item(self, itemtype: str, item_id: int, **params) -> Dict[str, Any]:
        """Get a single item from GLPI.

        Args:
            itemtype: Type of item (e.g., 'Ticket', 'Computer')
            item_id: ID of the item
            **params: Additional query parameters

        Returns:
            Item data as dictionary

        Raises:
            GLPIError: If request fails
        """
        url = f"{self.base_url}/{itemtype}/{item_id}"
        headers = self._get_headers(include_session=True)

        # Add all parameters to get full JSON response
        query_params = {
            "expand_dropdowns": "true",
            "get_hateoas": "false",
            "with_devices": "true",
            "with_disks": "true",
            "with_softwares": "true",
            "with_connections": "true",
            "with_networkports": "true",
            "with_infocoms": "true",
            "with_contracts": "true",
            "with_documents": "true",
            "with_tickets": "true",
            "with_problems": "true",
            "with_changes": "true",
            "with_notes": "true",
            "with_logs": "false",
            **params,
        }

        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def list_items(
        self, itemtype: str, range_start: int = 0, range_limit: int = 50, **params
    ) -> List[Dict[str, Any]]:
        """List items from GLPI with pagination.

        Args:
            itemtype: Type of items (e.g., 'Ticket', 'Computer')
            range_start: Start index for pagination
            range_limit: Number of items to retrieve
            **params: Additional query parameters

        Returns:
            List of items

        Raises:
            GLPIError: If request fails
        """
        url = f"{self.base_url}/{itemtype}"
        headers = self._get_headers(include_session=True)

        query_params = {
            "expand_dropdowns": "true",
            "get_hateoas": "false",
            "range": f"{range_start}-{range_start + range_limit - 1}",
            **params,
        }

        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # GLPI returns list directly for range queries
                return data if isinstance(data, list) else [data]
            elif response.status_code == 206:
                # Partial content (pagination)
                return response.json()
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def search_items(self, itemtype: str, criteria: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """Search items in GLPI with criteria.

        Args:
            itemtype: Type of items to search
            criteria: Search criteria (field, searchtype, value)

        Returns:
            List of matching items

        Raises:
            GLPIError: If request fails
        """
        url = f"{self.base_url}/search/{itemtype}"
        headers = self._get_headers(include_session=True)

        params = {"forcedisplay[0]": 1, "forcedisplay[1]": 2}  # Force display ID and name

        if criteria:
            for i, criterion in enumerate(criteria):
                params[f"criteria[{i}][field]"] = criterion.get("field", 1)
                params[f"criteria[{i}][searchtype]"] = criterion.get("searchtype", "contains")
                params[f"criteria[{i}][value]"] = criterion.get("value", "")

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def get_fingerprint(self, itemtype: str, item_id: int) -> Dict[str, Any]:
        """Get fingerprint field data from Plugin Fields for a specific item.

        Args:
            itemtype: Type of item (e.g., 'Problem', 'Ticket')
            item_id: ID of the item

        Returns:
            Fingerprint data as dictionary

        Raises:
            GLPIError: If request fails
        """
        # Construct the plugin field item type
        plugin_itemtype = f"PluginFields{itemtype}fingerprint"
        url = f"{self.base_url}/{plugin_itemtype}"
        headers = self._get_headers(include_session=True)

        params = {
            "expand_dropdowns": "true",
            "get_hateoas": "false",
            "searchText[items_id]": item_id,
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # Return first result if it's a list, otherwise return the item
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                return data
            elif response.status_code == 206:
                # Partial content (pagination)
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                return data
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def list_fingerprints(
        self, itemtype: str, range_start: int = 0, range_limit: int = 50, **params
    ) -> List[Dict[str, Any]]:
        """List fingerprint field data from Plugin Fields for an item type.

        Args:
            itemtype: Type of items (e.g., 'Problem', 'Ticket')
            range_start: Start index for pagination
            range_limit: Number of items to retrieve
            **params: Additional query parameters

        Returns:
            List of fingerprint records

        Raises:
            GLPIError: If request fails
        """
        # Construct the plugin field item type
        plugin_itemtype = f"PluginFields{itemtype}fingerprint"
        url = f"{self.base_url}/{plugin_itemtype}"
        headers = self._get_headers(include_session=True)

        query_params = {
            "expand_dropdowns": "true",
            "get_hateoas": "false",
            "range": f"{range_start}-{range_start + range_limit - 1}",
            **params,
        }

        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # GLPI returns list directly for range queries
                return data if isinstance(data, list) else [data]
            elif response.status_code == 206:
                # Partial content (pagination)
                return response.json()
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")

    def search_fingerprint(
        self, itemtype: str, fingerprint_value: str
    ) -> List[Dict[str, Any]]:
        """Search for items by fingerprint value using Plugin Fields search.

        Args:
            itemtype: Type of items (e.g., 'Problem', 'Ticket')
            fingerprint_value: The fingerprint value to search for

        Returns:
            List of matching fingerprint records

        Raises:
            GLPIError: If request fails
        """
        # Construct the plugin field item type
        plugin_itemtype = f"PluginFields{itemtype}fingerprint"
        url = f"{self.base_url}/search/{plugin_itemtype}"
        headers = self._get_headers(include_session=True)

        # Search by the fingerprint field (typically field ID 2 for custom field value)
        params = {
            "criteria[0][field]": 2,
            "criteria[0][searchtype]": "equals",
            "criteria[0][value]": fingerprint_value,
            "forcedisplay[0]": 1,
            "forcedisplay[1]": 2,
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                error_data = response.json() if response.text else {}
                raise_glpi_error(error_data, response.status_code)

        except requests.RequestException as e:
            raise GLPIError(f"Erro de conex\u00e3o: {str(e)}")
