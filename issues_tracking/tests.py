from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProjectTests(APITestCase):
    def setUp(self):
        self.user1_email = "test@test.com"
        self.user1_password = "testpassword"
        get_user_model().objects.create_user(
            email=self.user1_email, password=self.user1_password, username="test"
        )
        self.user2_email = "test2@test.com"
        self.user2_password = "testpassword2"
        get_user_model().objects.create_user(
            email=self.user2_email, password=self.user2_password, username="test2"
        )
        self.header1 = self.get_header_user(self.user1_email, self.user1_password)
        self.header2 = self.get_header_user(self.user2_email, self.user2_password)
        self.data = {
            "title": "test",
            "description": "test",
            "type": "BE",
        }

    def get_header_user(self, email, password):
        response = self.client.post(
            reverse("login"), {"email": email, "password": password}
        )
        access = response.json()["access"]
        header = {"Authorization": f"Bearer {access}"}
        return header

    def test_not_authenticated_create_project(self):
        response = self.client.post(
            reverse("projects-list"),
            {"title": "test", "description": "test", "type": "BE"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_create_project_successfull(self):
        response = self.client.post(
            reverse("projects-list"), data=self.data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_project_with_invalid_type(self):
        data = {
            "title": "test",
            "description": "test",
            "type": "invalid",
        }
        response = self.client.post(
            reverse("projects-list"), data=data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"type": ['"invalid" is not a valid choice.']}
        )

    def test_create_project_with_empty_title(self):
        data = {
            "title": "",
            "description": "test",
            "type": "BE",
        }
        response = self.client.post(
            reverse("projects-list"), data=data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"title": ["This field may not be blank."]})

    def test_create_project_with_empty_description(self):
        data = {
            "title": "test",
            "description": "",
            "type": "BE",
        }
        response = self.client.post(
            reverse("projects-list"), data=data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"description": ["This field may not be blank."]}
        )

    def test_create_project_with_empty_type(self):
        data = {
            "title": "test",
            "description": "test",
            "type": "",
        }
        response = self.client.post(
            reverse("projects-list"), data=data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"type": ['"" is not a valid choice.']})

    def test_list_projects_successfull(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.get(reverse("projects-list"), headers=self.header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_from_another_user(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.get(reverse("projects-list"), headers=self.header2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )
