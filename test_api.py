import unittest
import requests

class VaultShieldAPITests(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8080"  # Replace with your server's URL
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxOTIzODk0OSwianRpIjoiMDU1ZmZlOWUtYjVmNi00ZGQ3LWExYjYtOTZjYjllNDM3ZGU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQ0NjE4YjhmLWJiM2YtNDkwYy05ZDNmLTI1ODFlNjA4YzAwMC1jY2I3ZmIzNy1lOGYzLTRhNWEtODM3Ni05M2YyZjFlMTRlZGUiLCJuYmYiOjE3MTkyMzg5NDksImNzcmYiOiJmODc1ZDE5MS1kNTFiLTQwMjktYmM1My1iNzI4ODQ4YzAwNjQiLCJleHAiOjE3MTkyNDI1NDl9.D59HOQ6aclWfQHcKT9OGDp3pdf8dzVzP0cIO5Emm0l0"  # Replace with a valid token

    def setUp(self):
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json"
        }

    def test_register(self):
        url = f"{self.BASE_URL}/auth/register"
        payload = {
            "email": "autreuser@test.com",
            "password": "diofjlfgiuttttttt",
            "username": "sharecompte"
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_login(self):
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": "enzopenisson25@orange.fr",
            "password": "Azertytest!4577"
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_reset_password_otp(self):
        url = f"{self.BASE_URL}/auth/reset_password"
        payload = {"email": "enzopenisson25@orange.fr"}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("otp_sent", response.json())

    def test_change_password(self):
        url = f"{self.BASE_URL}/auth/change_password/some-uuid"
        payload = {
            "new_password": "NewPassword!123",
            "confirm_password": "NewPassword!123"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("password_changed", response.json())

    def test_add_vault(self):
        url = f"{self.BASE_URL}/vault/add"
        payload = {
            "uuidcategorie": None,
            "username": "lekekedu77",
            "email": "clementlol@gmail.com",
            "password": "jzezuongvotpnbdpf",
            "sitename": "canal",
            "urlsite": "https://canal.com",
            "urllogo": "https://canal.jpg",
            "note": "MDP canal plus"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("vault_added", response.json())

    def test_get_vault(self):
        url = f"{self.BASE_URL}/vault/getall"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_update_vault(self):
        url = f"{self.BASE_URL}/vault/update"
        payload = {
            "uuidCoffre": "1f6824d6-d0c5-4dd3-a9be-3f3130debed6-3fb99572-cd97-468e-9f59-261e154354e3",
            "secretkey": "j5jyX9LQq64s2Vk0_iRG7LWALqUsVHzF5_-QMs7yLH0=",
            "userUUid": "44618b8f-bb3f-490c-9d3f-2581e608c000-ccb7fb37-e8f3-4a5a-8376-93f2f1e14ede",
            "username": "michmich"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("vault_updated", response.json())

    def test_delete_vault(self):
        url = f"{self.BASE_URL}/vault/delete"
        payload = {"uuidCoffre": "1f6824d6-d0c5-4dd3-a9be-3f3130debed6-3fb99572-cd97-468e-9f59-261e154354e3"}
        response = requests.delete(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("vault_deleted", response.json())

if __name__ == "__main__":
    unittest.main()
