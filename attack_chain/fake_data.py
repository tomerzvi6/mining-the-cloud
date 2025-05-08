from faker import Faker

class FakeDataGenerator:
    def __init__(self):
        self.faker = Faker()

    def generate_log_entry(self):
        return f"[{self.faker.date_time()}] {self.faker.sentence()}"

    def generate_exfil_data(self):
        # Simulate exfiltrated data as a JSON string
        data = {
            "user": self.faker.user_name(),
            "email": self.faker.email(),
            "ip": self.faker.ipv4(),
            "payload": self.faker.text(max_nb_chars=200)
        }
        return str(data) 