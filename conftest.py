import pytest
from helpers.api_client import ApiClient

@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()

@pytest.fixture
def created_user(api_client):
    """Фикстура для создания и удаления пользователя"""
    email = api_client.generate_random_email()
    password = api_client.generate_random_string(8)
    name = api_client.generate_random_string(6)
    
    response = api_client.create_user(email=email, password=password, name=name)
    user_data = response.json()
    
    yield {"email": email,"password": password,"name": name,"token": user_data.get("accessToken"),"refresh_token": user_data.get("refreshToken")}
    
    if user_data.get("accessToken"):
        api_client.delete_user(user_data["accessToken"])

@pytest.fixture
def unique_user(api_client):
    """Фикстура для создания уникального пользователя с cleanup"""
    email = api_client.generate_random_email()
    password = api_client.generate_random_string(8)
    name = api_client.generate_random_string(6)
    
    response = api_client.create_user(email=email, password=password, name=name)
    user_data = response.json()
    
    yield {"email": email,"password": password,"name": name,"token": user_data.get("accessToken"),"response": response,"user_data": user_data}
    
    if user_data.get("accessToken"):
        api_client.delete_user(user_data["accessToken"])

@pytest.fixture
def ingredients_data(api_client):
    """Фикстура для получения ингредиентов"""
    response = api_client.get_ingredients()
    ingredients = response.json()["data"]
    return {"valid_ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]],"invalid_ingredient_hash": "invalid_hash_12345"}