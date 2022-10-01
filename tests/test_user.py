import pytest
from .fixtures import client, use_test_db_fixture, session_for_test, user_for_test
from cruds.users import generate_password_hash


@pytest.mark.usefixtures('use_test_db_fixture')
class TestUser:
    def test_signup(use_test_db_fixture):
        """
        サインアップを行う
        """
        name = 'hoge'
        email = 'test@test.co.jp'
        password = '12345'
        res = client.post('/api/v1/users/signup', json={
            'name': name,
            'email': email,
            'password': password
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json['name'] == name
        assert res_json['email'] == email

    def test_signup_exist_email(use_test_db_fixture, user_for_test):
        """
        すでにあるメールアドレスでサインアップを行う
        """
        name = 'hoge'
        email = 'test@test.com'
        password = '12345'
        res = client.post('/api/v1/users/signup', json={
            'name': name,
            'email': email,
            'password': password
        })

        assert res.status_code == 400, 'メールアドレスが既に存在している'
