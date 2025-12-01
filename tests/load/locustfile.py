from locust import HttpUser, task, between
import random
import time

class StudyTrackUser(HttpUser):
    wait_time = between(1, 3)  # cada usuario espera entre 1 y 3 secs entre requests
    last_subject_id = None
    last_session_id = None
    access_token = None
    headers = {}
    
    def on_start(self):
        """
        Esto corre cada vez que un usuario virtual comienza.
        1. Se registra
        2. Inicia sesión
        3. Guarda el token
        """
        # --- Registro ---
        register_payload = {
            "username": f"user_{random.randint(1, 999999)}",
            "email": f"user{random.randint(1, 999999)}@test.com",
            "password": "john123456",
            "confirm_password": "john123456"
        }
        self.client.post("/auth/register", json=register_payload)

        # --- Login ---
        login_payload = {
            "username": register_payload["username"],
            "password": "john123456"
        }
        login_res = self.client.post("/auth/login", json=login_payload)
        
        if login_res.status_code == 200:
            self.access_token = login_res.json().get("access_token")
        else:
            self.access_token = None

        self.headers = {"Authorization": f"Bearer {self.access_token}"}
    # -------------------------------------------------------------------
    # Helper: Exponential backoff for POST/PUT/DELETE
    # -------------------------------------------------------------------
    def request_with_backoff(self, method, url, **kwargs):
        delay = 1
        for attempt in range(5):
            res = self.client.request(method, url, **kwargs)
            if res.status_code == 429:
                time.sleep(delay)
                delay *= 2
            # Manejo de 404: no reintentar, solo loguear
            if res.status_code == 404:
                print(f"Recurso no encontrado: {url}")
                return res
            
            # Manejo de 403: loguear y salir
            if res.status_code == 403:
                print(f"Acceso prohibido: {url}")
                return res
            
            return res
        return res
    # -------------------------------------------------------------------
    #                              SUBJECTS
    # -------------------------------------------------------------------

    @task(2)  # más peso => se ejecuta más seguido
    def get_subjects(self):
        self.client.get("/subjects", headers=self.headers)

    @task(1)
    def create_subject(self):
        payload = {
            "name": f"Math {random.randint(1,999)}",
            "description": "test",
            "total_hours_goal": random.randint(10, 200),
            "total_hours_completed": 0,
            "priority_level": "HIGH",
            "status": "ACTIVE"
        }
        res = self.request_with_backoff("POST", "/subjects", json=payload, headers=self.headers)
        if res.status_code == 201:
            self.last_subject_id = res.json().get("id")

    @task(1)
    def update_subject(self):
        if self.last_subject_id is not None:
            # Verificar existencia antes de PUT
            check = self.client.get(f"/subjects/{self.last_subject_id}", headers=self.headers)
            if check.status_code == 200:
                payload = {
                    "name": "Updated Name",
                    "description": "Updated description",
                    "total_hours_goal": 150,
                    "total_hours_completed": 10,
                    "priority_level": "MEDIUM",
                    "status": "ACTIVE"
                }
                self.request_with_backoff("PUT", f"/subjects/{self.last_subject_id}", json=payload, headers=self.headers)

    @task(1)
    def delete_subject(self):
        if self.last_subject_id is not None:
            # Verificar existencia antes de DELETE
            check = self.client.get(f"/subjects/{self.last_subject_id}", headers=self.headers)
            if check.status_code == 200:
                self.request_with_backoff("DELETE", f"/subjects/{self.last_subject_id}", headers=self.headers)


    # -------------------------------------------------------------------
    #                              SESSIONS
    # -------------------------------------------------------------------

    @task(2)
    def get_sessions(self):
        self.client.get("/sessions", headers=self.headers)

    @task(1)
    def create_session(self):
        """
        Para crear una session, necesito subject_id.
        Si no hay, creo un subject primero.
        """
        if self.last_subject_id is None:
            # Creo subject automáticamente
            self.create_subject()

        payload = {
            "subject_id": self.last_subject_id,
            "start_time": "03:00PM",
            "end_time": "04:00PM",
            "notes": "Study session notes"
        }

        res = self.request_with_backoff("POST", "/sessions", json=payload, headers=self.headers)
        if res.status_code == 201:
            self.last_session_id = res.json().get("id")

    @task(1)
    def update_session(self):
        if self.last_session_id is not None:
            check = self.client.get(f"/sessions/{self.last_session_id}", headers=self.headers)
            if check.status_code == 200:
                payload = {
                    "subject_id": self.last_subject_id,
                    "start_time": "05:00PM",
                    "end_time": "06:00PM",
                    "notes": "Updated study session notes"
                }
                self.request_with_backoff("PUT", f"/sessions/{self.last_session_id}", json=payload, headers=self.headers)

    @task(1)
    def delete_session(self):
        if self.last_session_id is not None:
            check = self.client.get(f"/sessions/{self.last_session_id}", headers=self.headers)
            if check.status_code == 200:
                self.request_with_backoff("DELETE", f"/sessions/{self.last_session_id}", headers=self.headers)
