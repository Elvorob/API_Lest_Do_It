import pytest
import requests
import json
from http import HTTPStatus
# from collections import Counter


"""https://petstore.swagger.io/#/"""

base_url = "https://petstore.swagger.io/v2/"
msg = "======wrong status code======"

# =======================================================
# ========================= USER ========================
# =======================================================


@pytest.mark.post
def test_create_user():
    user_data = {
        "id": 123456,
        "username": "ElinaA",
        "firstName": "Elina",
        "lastName": "Ab",
        "email": "dgcvsjvuh@test.com",
        "password": "string123",
        "phone": "+15121234567",
        "userStatus": 0,
    }
    r = requests.post(f"{base_url}user", json=user_data)
    # print(r.json())
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.get
def test_logs_user_into_the_system():
    login_data = {
        "username": "ElinaA",
        "password": "string123",
    }
    r = requests.get(f"{base_url}user/login", json=login_data)
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.get
def test_logs_out_current_logged():
    r = requests.get(f"{base_url}user/logout")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.put
def test_update_user():
    update_data = {
        "id": 123456,
        "username": "ElinaA123",
        "firstName": "Elina123",
        "lastName": "Ab123",
        "email": "dgcvsjvuh@test.com",
        "password": "string123",
        "phone": "+15121234567",
        "userStatus": 0,
    }
    r = requests.put(f"{base_url}user/ElinaA", json=update_data)
    json_data = r.json()
    print(json.dumps(json_data, sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.get
def test_get_user_by_username():
    r = requests.get(f"{base_url}user/ElinaA123")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg
    json_data = r.json()
    expected_keys = ["email", "firstName", "id", "password"]
    json_list = []
    for key in json_data.keys():
        json_list.append(key)
    # print(json_list)
    assert (x in expected_keys for x in json_list), "======wrong keys======"


@pytest.mark.post
def test_create_with_list():
    create_data = [
        {
            "id": 1234567,
            "username": "ElinaA456",
            "firstName": "Elina456",
            "lastName": "Ab456",
            "email": "dgcvsjvuha@test.com",
            "password": "string123",
            "phone": "+15121234567",
            "userStatus": 0,
        },
        {
            "id": 397656,
            "username": "Sofi",
            "firstName": "Sofia",
            "lastName": "Ab",
            "email": "kjfve@test.com",
            "password": "string123",
            "phone": "+15127654321",
            "userStatus": 0,
        },
    ]
    r = requests.post(f"{base_url}user/createWithList", json=create_data)
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.delete
def test_delete_user():
    r = requests.delete(f"{base_url}user/ElinaA123")
    assert r.status_code == HTTPStatus.OK, msg
    r = requests.get(f"{base_url}user/ElinaA")
    assert r.status_code == HTTPStatus.NOT_FOUND, msg


# =======================================================
# ========================= PET =========================
# =======================================================


@pytest.mark.post
def test_add_new_pet():
    pet_data = {
        "id": 10001,
        "category": {"id": 987, "name": "crocodile"},
        "name": "fluffy",
        "photoUrls": ["/Users/elinaa/Desktop/PNG-Picture.png"],
        "tags": [{"id": 0, "name": "string111"}],
        "status": "available",
    }
    r = requests.post(f"{base_url}pet", json=pet_data)
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.skip(reason="FileNotFoundError")
@pytest.mark.post
def test_upload_image():
    file = {
        "additionalMetadata": "new photo",
        "file": open("/Users/elinaa/Desktop/PNG-Picture.png", "rb"),
    }
    r = requests.post(f"{base_url}pet/10001/uploadImage", files=file)
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.get
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pets_by_status(status):
    r = requests.get(f"{base_url}pet/findByStatus?status={status}")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg
    json_data = r.json()
    json_keys = []
    for elem in json_data:
        for k in elem.keys():
            json_keys.append(k)
    expected_keys = ["id", "name", "status"]
    assert (x in expected_keys for x in json_keys), "======wrong keys======"


@pytest.mark.get
def test_find_pet_by_id():
    r = requests.get(f"{base_url}pet/10001")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.post
@pytest.mark.skip(reason="415 Unsupported Media Type")
def test_update_pet():
    pet_update = {"name": "fluffy2", "status": "sold"}
    r = requests.post(f"{base_url}pet/10001", json=pet_update)
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.delete
def test_delete_pet():
    r = requests.delete(f"{base_url}pet/10001")
    assert r.status_code == HTTPStatus.OK, msg
    r = requests.get(f"{base_url}pet/10001")
    assert r.status_code == HTTPStatus.NOT_FOUND, msg


# =======================================================
# ======================== STORE ========================
# =======================================================


@pytest.mark.post
def test_place_order_for_pet():
    order_data = {
        "id": 9,
        "petId": 10001,
        "quantity": 1,
        "shipDate": "2022-12-09T00:46:53.139Z",
        "status": "placed",
        "complete": True,
    }
    r = requests.post(f"{base_url}store/order", json=order_data)
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.get
def test_find_order():
    r = requests.get(f"{base_url}store/order/9")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg


@pytest.mark.delete
def test_delete_order():
    r = requests.delete(f"{base_url}store/order/9")
    # print(json.dumps(r.json(), sort_keys=True, indent=4))
    assert r.status_code == HTTPStatus.OK, msg
    r = requests.get(f"{base_url}store/order/9")
    assert r.status_code == HTTPStatus.NOT_FOUND, msg
