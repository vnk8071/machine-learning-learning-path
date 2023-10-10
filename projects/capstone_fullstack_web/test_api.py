import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from database.models import setup_db, db_drop_and_create_all, Drink, Ingredient, Property
from logger import Logger
from settings import DB_USER, DB_PASSWORD
from api import create_app

logger = Logger.get_logger(__name__)
barista_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOiJodHRwczovL2Rldi10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTIxMjlkMjQxOTkzYmQ4ODgwMmJkNmQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvbG9naW4iLCJpYXQiOjE2OTY4NjAzMTcsImV4cCI6MTY5Njg2NzUxNywiYXpwIjoiS3pRYjRmV2JKMGJET3dvM01PZEcwdWN6MFR2dHUyU1oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbmdyZWRpZW50cyJdfQ.aULs60rKj97d1kzPkx6CFWdAjhhF7kYC-fNCm7zOUECFg_blYQBN89hWvIyyTB8hDVFn_uV0fO4RzHB87TKlEBkdve3otK1CSDOEuRril7vzlyU_sGHBnD-MgQocvttunYOLxSKZhEhOsn0AZ0jlIzoK1azLI3lb5oaRNCl5VCNV10qv1HEOMRQXFJSQKf-alZwlsa1J-Q8QpO06fvWAAfmKIPU4u3zkDj6hzNEiuSXga-0BVfM5MaVKKnwMi4v8mK-Cud4xn0Vn3XUBsqlIRLmAZGts8d9uexWufqzeBHFSWJr6YwIARKMv48pSdOaNBT3v7LxIkg_8cL0VNWbE4g'
}

manager_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOiJodHRwczovL2Rldi10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5Njg2MDI1MiwiZXhwIjoxNjk2ODY3NDUyLCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImRlbGV0ZTppbmdyZWRpZW50cyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbmdyZWRpZW50cyIsInBhdGNoOmRyaW5rcyIsInBhdGNoOmluZ3JlZGllbnRzIiwicG9zdDpkcmlua3MiLCJwb3N0OmluZ3JlZGllbnRzIl19.vk92gBaCaVRLeL_sn3cE-x8eR7acI740xr6RZyfvTplym1k2Gj0if65oNi2ByTp1H8bRVCxEk_nD-mF5qpKW2jovJMDjXMwANc-AAjQkQQRHmcwn7wMH9IJo1V2DlN5OoGi1fvB1YUDDG89QB1xsPcvBGdP68ckC2GiqAqYX3sR0PLwvM3IuLNYc0vpyPsVBZJcsMEenQQPj0myH18m2sgfS8m4-8ifrljzuZ4E5xCAFy7sxtso66vqgDxQg9aZwLosaHtsY1HpPnihE8I_rDRnBlFzQQIl7o5CjBbtG3XE5Xhq5IYlOpSt2hpXaWKd8gABj8TtDg98JNvPElvZieg'
}

fake_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOKhoiVN10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5NjgzODc2NCwiZXhwIjoxNjk2ODQ1OTY0LCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.Nkm0-htqUxFozmhGpHYGDvfLIslrPFLb06h3WUx_v2H1dmwbyQVfDpileF0VtTWTYG4_Ygmwq3axFkFCkS1zG-Dq7O9ajLfz41ZDhnb9wb_hQx0IVCZVl8JfaPSylVRnGPMWzkOw5zRNM7_MUt5oHcKQxQa21w73Pew7HQbZzQrYPhvjHv4RIUo4MxE6IWMlzKLMBjiV74qYY0PTa7SfN4CaCFnBWe1-DovlB_CMl36DChGXlUj30rQwtwtG_kesZUOL3mS_e28D9unNeylWbKNr5MvVAOVs9_CnWiXvhpKKx4gKhr_OZUOvW8uYv-KPzRAMMzTRBPeCek-C1gf3wg'
}


class CoffeeShopTestCase(unittest.TestCase):
    """This class represents the drink api test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test=True)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.database_name = "drink_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            DB_USER,
            DB_PASSWORD,
            'localhost:5432',
            self.database_name
        )
        setup_db(app=self.app, database_path=self.database_path)
        with self.app.app_context():
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_root(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)

    def test_get_drinks_barista(self):
        response = self.client.get('/drinks', headers=barista_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_manager(self):
        response = self.client.get('/drinks', headers=manager_auth_header)
        logger.info(response)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_fake(self):
        response = self.client.get('/drinks', headers=fake_auth_header)
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_get_drink_items(self):
        response = self.client.get('/drinks/1', headers=barista_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_fail(self):
        response = self.client.get('/drinks', headers={})
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_get_drinks_detail_barista(self):
        response = self.client.get(
            '/drinks-detail',
            headers=barista_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_detail_manager(self):
        response = self.client.get(
            '/drinks-detail',
            headers=manager_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_drinks_detail_fake(self):
        response = self.client.get('/drinks-detail', headers=fake_auth_header)
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_get_drinks_detail_fail(self):
        response = self.client.get('/drinks-detail', headers={})
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_post_drinks_manager(self):
        response = self.client.post(
            '/drinks',
            headers=manager_auth_header,
            json={
                'title': 'Coffee',
                'recipe': '[{"name": "Coffee", "color": "black", "parts": 1}]'})
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_drinks_barista(self):
        response = self.client.post(
            '/drinks',
            headers=barista_auth_header,
            json={
                'title': 'water',
                'recipe': '[{"name": "water", "color": "blue", "parts": 1}'})
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_post_drinks_fake(self):
        response = self.client.post('/drinks', headers=fake_auth_header, json={
            'title': 'water',
            'recipe': '[{"name": "water", "color": "blue", "parts": 1}'
        })
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_post_drinks_fail(self):
        response = self.client.post('/drinks', headers={}, json={
            'title': 'water',
            'recipe': '[{"name": "water", "color": "blue", "parts": 1}'
        })
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_patch_drinks_manager(self):
        response = self.client.patch(
            '/drinks/1',
            headers=manager_auth_header,
            json={
                'title': 'water',
                'recipe': '[{"name": "water", "color": "green", "parts": 1}]'})
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_drinks_barista(self):
        response = self.client.patch(
            '/drinks/1',
            headers=barista_auth_header,
            json={
                'title': 'water',
                'recipe': '[{"name": "water", "color": "green", "parts": 1}]'})
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_patch_drinks_fail(self):
        response = self.client.patch('/drinks/1', headers={}, json={
            'title': 'water',
            'recipe': '[{"name": "water", "color": "green", "parts": 1}]'
        })
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_delete_drinks_manager(self):
        response = self.client.delete('/drinks/1', headers=manager_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_drinks_barista(self):
        response = self.client.delete('/drinks/1', headers=barista_auth_header)
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_delete_drinks_fail(self):
        response = self.client.delete('/drinks/1', headers={})
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_get_ingredients_barista(self):
        response = self.client.get('/ingredients', headers=barista_auth_header)
        logger.info(f">>>>> {response}")
        self.assertEqual(response.status_code, 200)

    def test_get_ingredients_manager(self):
        response = self.client.get('/ingredients', headers=manager_auth_header)
        logger.info(f"<<< {response}")
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_ingredients_fail(self):
        response = self.client.get('/ingredients', headers={})
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_post_ingredients_manager(self):
        response = self.client.post(
            '/ingredients',
            headers=manager_auth_header,
            json={
                'name': 'Matcha',
                'density': '90%'})
        logger.info(f">>>>> {response}")
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_ingredients_barista(self):
        response = self.client.post(
            '/ingredients',
            headers=barista_auth_header,
            json={
                'name': 'Matcha',
                'density': '90%'})
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_post_ingredients_fail(self):
        response = self.client.post('/ingredients', headers={}, json={
            'name': 'Matcha',
            'density': '90%'
        })
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_patch_ingredients_manager(self):
        response = self.client.patch(
            '/ingredients/1',
            headers=manager_auth_header,
            json={
                'name': 'water',
                'density': '80%'})
        logger.info(f">>>>><<<<< {response}")
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_ingredients_barista(self):
        response = self.client.patch(
            '/ingredients/1',
            headers=barista_auth_header,
            json={
                'name': 'water',
                'density': '80%'})
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_patch_ingredients_fail(self):
        response = self.client.patch('/ingredients/1', headers={}, json={
            'name': 'water',
            'density': '80%'
        })
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_delete_ingredients_manager(self):
        response = self.client.delete(
            '/ingredients/1', headers=manager_auth_header)
        data = json.loads(response.data)
        logger.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_ingredients_barista(self):
        response = self.client.delete(
            '/ingredients/1', headers=barista_auth_header)
        logger.info(response.data)
        self.assertEqual(response.status_code, 403)

    def test_delete_ingredients_fail(self):
        response = self.client.delete('/ingredients/1', headers={})
        logger.info(response.data)
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
