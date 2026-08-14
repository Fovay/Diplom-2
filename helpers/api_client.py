import requests
import random
import string

class ApiClient:
    BASE_URL = "https://stellarburgers.education-services.ru/api"

    def __init__(self):
        self.session = requests.Session()

    def create_user(self, email=None, password=None, name=None):
        """Создание пользователя с генерацией недостающих полей"""
        if email is None:
            email = self.generate_random_email()
        if password is None:
            password = self.generate_random_string(8)
        if name is None:
            name = self.generate_random_string(6)

        payload = {"email": email,"password": password,"name": name}
        response = self.session.post(f"{self.BASE_URL}/auth/register", json=payload)
        return response

    def create_user_without_field(self, missing_field='email'):
        """Создание пользователя с отсутствующим обязательным полем"""
        payload = {"email": self.generate_random_email(),"password": self.generate_random_string(8),"name": self.generate_random_string(6)}
        
        if missing_field in payload:
            del payload[missing_field]
        response = self.session.post(f"{self.BASE_URL}/auth/register", json=payload)
        return response

    def login_user(self, email, password):
        """Логин пользователя"""
        payload = {"email": email,"password": password}
        response = self.session.post(f"{self.BASE_URL}/auth/login", json=payload)
        return response

    def get_ingredients(self):
        """Получение списка ингредиентов"""
        response = self.session.get(f"{self.BASE_URL}/ingredients")
        return response

    def create_order(self, ingredients, token=None):
        """Создание заказа"""
        headers = {}
        if token:
            headers["Authorization"] = token
        payload = {"ingredients": ingredients}
        response = self.session.post(f"{self.BASE_URL}/orders", json=payload, headers=headers)
        return response

    def delete_user(self, token):
        """Удаление пользователя"""
        headers = {"Authorization": token}
        response = self.session.delete(f"{self.BASE_URL}/auth/user", headers=headers)
        return response

    @staticmethod
    def generate_random_string(length):
        """Генерация случайной строки"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_email():
        """Генерация случайного email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_{random_string}@yandex.ru"