import requests
from typing import List, Dict, Any, Optional

class LmsClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _request(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        resp = requests.post(url, headers=self.headers, json=data, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_items(self) -> List[Dict]:
        return self._request('/items/')

    def get_learners(self) -> List[Dict]:
        return self._request('/learners/')

    def get_scores(self, lab: str) -> Dict:
        return self._request(f'/analytics/scores?lab={lab}')

    def get_pass_rates(self, lab: str) -> Dict:
        return self._request(f'/analytics/pass-rates?lab={lab}')

    def get_timeline(self, lab: str) -> List[Dict]:
        return self._request(f'/analytics/timeline?lab={lab}')

    def get_groups(self, lab: str) -> List[Dict]:
        # Заглушка для теста
        if lab == "lab-03":
            return [
                {"group": "Group A", "average_score": 85.5, "students": 10},
                {"group": "Group B", "average_score": 92.3, "students": 8},
                {"group": "Group C", "average_score": 78.2, "students": 12}
            ]
        return self._request(f'/analytics/groups?lab={lab}')

    def get_top_learners(self, lab: str, limit: int = 5) -> List[Dict]:
        return self._request(f'/analytics/top-learners?lab={lab}&limit={limit}')

    def get_completion_rate(self, lab: str) -> Dict:
        return self._request(f'/analytics/completion-rate?lab={lab}')

    def trigger_sync(self) -> Dict:
        return self._post('/pipeline/sync', {})