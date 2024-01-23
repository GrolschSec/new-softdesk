from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSignUp(APITestCase):
    def setUp(self):
        self.url = reverse("signup")
        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "john-doe@gmail.com"
        self.password = "pas1Mais2!"

    def test_signup_successfull(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalid_email(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": "john-doe",
            "password": self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_empty_email(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": "",
            "password": self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["This field may not be blank."]})

    def test_signup_email_already_exist(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"email": ["User with this email already exists"]}
        )

    def test_signup_empty_password(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["This field may not be blank."]}
        )

    def test_signup_password_too_short(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "Pas1!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "password": [
                    "This password is too short. It must contain at least 8 characters."
                ]
            },
        )

    def test_signup_password_no_uppercase(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "pas1mais2!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"password": ["This password must contain at least 1 uppercase letter."]},
        )

    def test_signup_password_no_lowercase(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "PAS1MAIS2!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"password": ["This password must contain at least 1 lowercase letter."]},
        )

    def test_signup_password_no_digit(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "PasMais!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"password": ["This password must contain at least 1 number."]},
        )

    def test_signup_password_no_special_character(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "PasMais6",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"password": ["This password must contain at least 1 special character."]},
        )


class TestLogin(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "john-doe@gmail.com"
        self.password = "pas1Mais2!"
        self.client.post(
            self.signup_url,
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "password": self.password,
            },
        )

    def test_login_successfull(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_email(self):
        data = {"email": "john-doe", "password": self.password}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Enter a valid email address."]})

    def test_login_empty_email(self):
        data = {"email": "", "password": self.password}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["This field may not be blank."]})

    def test_login_empty_password(self):
        data = {"email": self.email, "password": ""}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["This field may not be blank."]}
        )

    def test_login_invalid_credentials(self):
        data = {"email": self.email, "password": "pas1Mais2"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Invalid email/password"})
