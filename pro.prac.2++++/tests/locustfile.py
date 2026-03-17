from locust import HttpUser, between, task


class DashboardUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def load_home_page(self):
        self.client.get("/")

    @task(1)
    def load_dash_layout(self):
        self.client.get("/_dash-layout")

    @task(1)
    def load_dash_dependencies(self):
        self.client.get("/_dash-dependencies")
