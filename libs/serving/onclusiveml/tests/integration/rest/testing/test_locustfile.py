# 3rd party libraries
from locust import HttpUser, between, task


class TestWebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task()
    def get_home_page(self):
        """
        Gets /
        """
        self.client.get("/")
