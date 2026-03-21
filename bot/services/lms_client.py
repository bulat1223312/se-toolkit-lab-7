import requests
from typing import List, Dict, Any, Optional

class LmsClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}{endpoint}"
        resp = requests.get(url, headers=self.headers, timeout=5)
        resp.raise_for_status()
        return resp.json()

    def get_items(self) -> List[Dict]:
        """Возвращает список всех items (лабораторные и задачи)."""
        return self._request('/items/')

    def get_labs(self) -> List[Dict]:
        """Возвращает только лабораторные работы (type == 'lab')."""
        items = self.get_items()
        return [item for item in items if item.get('type') == 'lab']

    def get_pass_rates(self, lab_id: str) -> Dict:
        """Возвращает словарь с pass rates для лабораторной."""
        return self._request(f'/analytics/pass-rates?lab={lab_id}')