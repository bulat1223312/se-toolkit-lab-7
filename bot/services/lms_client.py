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
        """Выполняет GET-запрос и возвращает JSON или None при ошибке."""
        try:
            url = f"{self.base_url}{endpoint}"
            resp = requests.get(url, headers=self.headers, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            # Сохраняем детали ошибки для дальнейшего форматирования
            raise  # Мы перехватим выше и преобразуем

    def get_items(self) -> Optional[List[Dict]]:
        """Возвращает список всех items или None при ошибке."""
        try:
            return self._request('/items/')
        except requests.exceptions.RequestException as e:
            raise

    def get_pass_rates(self, lab_id: str) -> Optional[Dict]:
        """Возвращает pass rates для лабораторной или None при ошибке."""
        try:
            return self._request(f'/analytics/pass-rates?lab={lab_id}')
        except requests.exceptions.RequestException as e:
            raise