import unittest
import requests

class VaultShieldAPITests(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8080"  # Remplacez par l'URL de votre serveur
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxOTIzODk0OSwianRpIjoiMDU1ZmZlOWUtYjVmNi00ZGQ3LWExYjYtOTZjYjllNDM3ZGU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQ0NjE4YjhmLWJiM2YtNDkwYy05ZDNmLTI1ODFlNjA4YzAwMC1jY2I3ZmIzNy1lOGYzLTRhNWEtODM3Ni05M2YyZjFlMTRlZGUiLCJuYmYiOjE3MTkyMzg5NDksImNzcmYiOiJmODc1ZDE5MS1kNTFiLTQwMjktYmM1My1iNzI4ODQ4YzAwNjQiLCJleHAiOjE3MTkyNDI1NDl9.D59HOQ6aclWfQHcKT9OGDp3pdf8dzVzP0cIO5Emm0l0"  # Remplacez par un jeton valide

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
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_login(self):
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": "enzopenisson25@orange.fr",
            "password": "Azertytest!4577"
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_logout(self):
        url = f"{self.BASE_URL}/auth/logout"
        response = requests.post(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_reset_password_otp(self):
        url = f"{self.BASE_URL}/auth/reset_password"
        payload = {"email": "enzopenisson25@orange.fr"}
        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_verify_otp(self):
        url = f"{self.BASE_URL}/auth/verify_otp"
        payload = {
            "email": "enzopenisson25@orange.fr",
            "otp": "99085087"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_change_password(self):
        url = f"{self.BASE_URL}/auth/change_password/0d8180ec-310d-4ae9-874c-e7f2414c9df2-49983183-1513-47b6-978e-2af06d5f097a-aca0ac53-a318-4b86-a52b-4362e6457a79-1303b492-d640-4bda-a02a-579f581322ba"
        payload = {
            "new_password": "Azertytest!4577",
            "confirm_password": "Azertytest!4577"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_list_user_admin(self):
        url = f"{self.BASE_URL}/admin/listadmin"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_set_user_admin(self):
        url = f"{self.BASE_URL}/admin/setadmin"
        payload = {"email": "autreuser@test.com"}
        response = requests.put(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_list_all_mdp(self):
        url = f"{self.BASE_URL}/admin/listvault"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

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
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_get_vault(self):
        url = f"{self.BASE_URL}/vault/getall"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_get_coffre_info(self):
        url = f"{self.BASE_URL}/vault/get"
        payload = {
            "uuidCoffre": "9c6d4504-01bb-49e4-b286-72744b905cf3-7ad6394a-82bb-4e36-b107-c48e704f9d69",
            "secretkey": "1J5KsyRPmOnxhjDRhfnPZusjcum_nGtej7u2wERTFzM="
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

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
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_delete_vault(self):
        url = f"{self.BASE_URL}/vault/delete"
        payload = {"uuidCoffre": "1f6824d6-d0c5-4dd3-a9be-3f3130debed6-3fb99572-cd97-468e-9f59-261e154354e3"}
        response = requests.delete(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

    def test_get_secret_key(self):
        url = f"{self.BASE_URL}/vault/secretkey"
        payload = {"uuidCoffre": "49ce422c-d21e-4c3c-9920-b5c6b79b8f79-70effc1d-eacf-44b0-a13c-0bbac9fd0f07"}
        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Ajoutez d'autres assertions selon la réponse attendue

if __name__ == "__main__":
    unittest.main()
