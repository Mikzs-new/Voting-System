import requests
from typing import Dict, List, Any, Optional
from config import (
    API_BASE_URL,
    AUTH_URL,
    JWT_AUTH_URLS,
    LOGOUT_URL,
    SESSION_TIMEOUT,
    TOKEN_AUTH_URLS,
)
from logger_setup import LOGGER

class APIClient:
    """Handles all API communication with the Django backend"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = API_BASE_URL
        self.auth_url = AUTH_URL
        self.is_authenticated = False
        self.current_user = None
        self.auth_mode = None
        self.timeout = SESSION_TIMEOUT * 60
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate with the Django backend"""
        LOGGER.info("Login attempt for user=%s", username)
        try:
            self.session = requests.Session()
            if self._login_with_jwt(username, password):
                return True

            if self._login_with_token(username, password):
                return True

            if self._login_with_session(username, password):
                return True

            LOGGER.warning("Login failed for user=%s", username)
            return False
            
        except requests.exceptions.RequestException:
            LOGGER.exception("Connection error during login for user=%s", username)
            return False

    def guest_login(self, username: str, password: str) -> bool:
        """Allow desktop access without backend authentication."""
        recorded_username = username if username else "Guest"
        self.session = requests.Session()
        self.is_authenticated = True
        self.current_user = recorded_username
        self.auth_mode = "guest"
        LOGGER.info(
            "Guest desktop login accepted user=%s password_length=%s",
            recorded_username,
            len(password or ""),
        )
        return True

    def _login_with_jwt(self, username: str, password: str) -> bool:
        payload = {'username': username, 'password': password}
        for auth_url in JWT_AUTH_URLS:
            try:
                response = self.session.post(auth_url, json=payload, timeout=30)
                if response.status_code != 200:
                    continue

                data = response.json()
                token = data.get('access') or data.get('token')
                if not token:
                    continue

                self.session.headers.update({'Authorization': f'Bearer {token}'})
                if self._can_access_api():
                    self.is_authenticated = True
                    self.current_user = username
                    self.auth_mode = "jwt"
                    LOGGER.info("Login succeeded for user=%s using JWT endpoint=%s", username, auth_url)
                    return True
            except requests.exceptions.RequestException:
                continue
        return False

    def _login_with_token(self, username: str, password: str) -> bool:
        payload = {'username': username, 'password': password}
        for auth_url in TOKEN_AUTH_URLS:
            try:
                response = self.session.post(auth_url, json=payload, timeout=30)
                if response.status_code != 200:
                    continue

                data = response.json()
                token = data.get('token')
                if not token:
                    continue

                self.session.headers.update({'Authorization': f'Token {token}'})
                if self._can_access_api():
                    self.is_authenticated = True
                    self.current_user = username
                    self.auth_mode = "token"
                    LOGGER.info("Login succeeded for user=%s using token endpoint=%s", username, auth_url)
                    return True
            except requests.exceptions.RequestException:
                continue
        return False

    def _login_with_session(self, username: str, password: str) -> bool:
        login_data = {'username': username, 'password': password}
        response = self.session.post(self.auth_url, data=login_data, timeout=30)
        if response.status_code not in (200, 302):
            return False

        if self._can_access_api():
            self.is_authenticated = True
            self.current_user = username
            self.auth_mode = "session"
            LOGGER.info("Login succeeded for user=%s using session auth", username)
            return True
        return False

    def _can_access_api(self) -> bool:
        test_response = self.session.get(f"{self.base_url}students/", timeout=10)
        return test_response.status_code == 200
    
    def logout(self):
        """Logout from the backend"""
        try:
            self.session.get(LOGOUT_URL, timeout=10)
            LOGGER.info("Logout succeeded for user=%s", self.current_user)
        except requests.exceptions.RequestException:
            LOGGER.exception("Logout request failed for user=%s", self.current_user)
        finally:
            self.is_authenticated = False
            self.current_user = None
            self.auth_mode = None
            self.session = requests.Session()
    
    def _request(self, method: str, endpoint: str, data: Any = None, params: Any = None) -> Optional[Any]:
        """Make an API request"""
        if not self.is_authenticated:
            LOGGER.warning("Rejected unauthenticated request method=%s endpoint=%s", method, endpoint)
            return None
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            elif method == 'PUT':
                response = self.session.put(url, json=data, timeout=30)
            elif method == 'DELETE':
                response = self.session.delete(url, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if response.status_code in [200, 201, 204]:
                if response.content:
                    return response.json()
                return True
            else:
                LOGGER.error(
                    "API error method=%s endpoint=%s status=%s body=%s",
                    method,
                    endpoint,
                    response.status_code,
                    response.text[:500],
                )
                return None
                
        except requests.exceptions.RequestException:
            LOGGER.exception("Request error method=%s endpoint=%s", method, endpoint)
            return None
    
    def get(self, endpoint: str, params: Dict = None) -> Optional[List[Dict]]:
        """GET request"""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """POST request"""
        return self._request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """PUT request"""
        return self._request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> bool:
        """DELETE request"""
        return self._request('DELETE', endpoint) is not None
    
    # Specific API endpoints
    def get_students(self) -> Optional[List[Dict]]:
        return self.get('students/')
    
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        return self.post('students/', student_data)
    
    def update_student(self, student_id: int, student_data: Dict) -> Optional[Dict]:
        return self.put(f'students/{student_id}/', student_data)
    
    def delete_student(self, student_id: int) -> bool:
        return self.delete(f'students/{student_id}/')
    
    def get_courses(self) -> Optional[List[Dict]]:
        return self.get('courses/')
    
    def get_elections(self) -> Optional[List[Dict]]:
        return self.get('elections/')
    
    def create_election(self, election_data: Dict) -> Optional[Dict]:
        return self.post('elections/', election_data)
    
    def get_candidates(self) -> Optional[List[Dict]]:
        return self.get('candidates/')
    
    def create_candidate(self, candidate_data: Dict) -> Optional[Dict]:
        LOGGER.info(
            "Submitting candidate user=%s student_id=%s election=%s",
            self.current_user,
            candidate_data.get('student_id'),
            candidate_data.get('election'),
        )
        result = self.post('candidates/', candidate_data)
        if result:
            LOGGER.info(
                "Candidate synced user=%s candidate_id=%s",
                self.current_user,
                result.get('id'),
            )
        return result
    
    def get_positions(self) -> Optional[List[Dict]]:
        return self.get('positions/')
    
    def create_position(self, position_data: Dict) -> Optional[Dict]:
        return self.post('positions/', position_data)
    
    def get_partylists(self) -> Optional[List[Dict]]:
        return self.get('partylists/')
    
    def get_votes(self) -> Optional[List[Dict]]:
        return self.get('votes/')

    def create_vote(self, vote_data: Dict) -> Optional[Dict]:
        LOGGER.info(
            "Submitting vote user=%s student_id=%s election=%s",
            self.current_user,
            vote_data.get('student_id'),
            vote_data.get('election'),
        )
        result = self.post('votes/', vote_data)
        if result:
            LOGGER.info(
                "Vote synced user=%s vote_id=%s",
                self.current_user,
                result.get('id'),
            )
        return result
    
    def get_school_year_elections(self) -> Optional[List[Dict]]:
        return self.get('school_year_elections/')
    
    def get_statistics(self) -> Dict:
        """Get various statistics"""
        stats = {}
        
        students = self.get_students()
        stats['total_students'] = len(students) if students else 0
        
        elections = self.get_elections()
        stats['total_elections'] = len(elections) if elections else 0
        
        votes = self.get_votes()
        stats['total_votes'] = len(votes) if votes else 0
        
        candidates = self.get_candidates()
        stats['total_candidates'] = len(candidates) if candidates else 0
        
        if stats['total_students'] > 0:
            stats['turnout_percentage'] = (stats['total_votes'] / stats['total_students']) * 100
        else:
            stats['turnout_percentage'] = 0
        
        return stats
