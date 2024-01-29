from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class IssuesTrackingTestCase(APITestCase):
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


class ProjectTests(IssuesTrackingTestCase):
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

    def test_retrieve_project_successfull(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.get(
            reverse("projects-detail", args=[1]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project_from_another_user(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.get(
            reverse("projects-detail", args=[1]), headers=self.header2
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_retrieve_project_does_not_exist(self):
        response = self.client.get(
            reverse("projects-detail", args=[1]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_update_project_successfull(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.put(
            reverse("projects-detail", args=[1]), data=self.data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_project_from_another_user(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.put(
            reverse("projects-detail", args=[1]), data=self.data, headers=self.header2
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_update_project_does_not_exist(self):
        response = self.client.put(
            reverse("projects-detail", args=[1]), data=self.data, headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_delete_project_successfull(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.delete(
            reverse("projects-detail", args=[1]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_from_another_user(self):
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)
        response = self.client.delete(
            reverse("projects-detail", args=[1]), headers=self.header2
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_delete_project_does_not_exist(self):
        response = self.client.delete(
            reverse("projects-detail", args=[1]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Not found."})


class ContributorTests(IssuesTrackingTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse("projects-list"), data=self.data, headers=self.header1)

    def test_add_contributor_successfull(self):
        response = self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_contributor_already_exist(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["This contributor already exists in this project"]},
        )

    def test_add_contributor_not_authorized(self):
        response = self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header2,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_add_contributor_project_does_not_exist(self):
        response = self.client.post(
            reverse("project-contributors-list", args=[2]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_contributor_from_author(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.get(
            reverse("project-contributors-list", args=[1]),
            headers=self.header1,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contributor_from_contributor(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.get(
            reverse("project-contributors-list", args=[1]),
            headers=self.header2,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contributor_from_another_user(self):
        response = self.client.get(
            reverse("project-contributors-list", args=[1]),
            headers=self.header2,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_contributor_project_does_not_exist(self):
        response = self.client.get(
            reverse("project-contributors-list", args=[2]),
            headers=self.header1,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_contributor_successfull(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.delete(
            reverse("project-contributors-detail", args=[1, 2]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_contributor_from_another_user(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.delete(
            reverse("project-contributors-detail", args=[1, 2]), headers=self.header2
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_contributor_project_does_not_exist(self):
        response = self.client.delete(
            reverse("project-contributors-detail", args=[2, 2]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_contributor_contributor_does_not_exist(self):
        response = self.client.delete(
            reverse("project-contributors-detail", args=[1, 2]), headers=self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_contributor_author(self):
        self.client.post(
            reverse("project-contributors-list", args=[1]),
            data={"user": 2, "permission": "LOW", "role": "Lead Dev"},
            headers=self.header1,
        )
        response = self.client.get(
            reverse("project-contributors-detail", args=[1, 2]), headers=self.header1
        )
        self.assertEqual(
            response.json(), {"detail": "Retrieve operation is not allowed"}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
