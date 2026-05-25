from locust import HttpUser, task, between

class LibraryLoadTestUser(HttpUser):
    # Імітація реальної поведінки: користувач чекає від 1 до 3 секунд між запитами
    wait_time = between(1, 3)

    @task
    def view_books(self):
        # Locust автоматично підставить базовий URL сервера (ми вкажемо його в Docker)
        with self.client.get("/books/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")