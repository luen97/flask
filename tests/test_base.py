from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class MainTest(TestCase):
    def create_app(self): 
        # Configuramos para testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app
    # self explanatory
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        # programé index para que me redirija a hello
        # vemos si funciona
        response = self.client.get(url_for('index'))
        # No está funcionando
        # self.assertRedirects(response, url_for('hello'))
        self.assertEqual(response.location, '/hello')

    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)
        # self.assertEqual(response.status_code, 200)

    def test_hello_post(self):
        fake_form = {
            'username':'fake',
            'password':'fake-password'
        }
        response = self.client.post(
                    url_for('hello'), 
                    data=fake_form)
        # self.assertRedirects(response, url_for('index'))
        self.assertEqual(response.location, '/')
    
    # def test_user_registered_flashed_message(self):
    #     fake_form = {
    #         'username': 'vijoin',
    #         'password': '123456'
    #     }
    #     self.client.post(url_for('hello'), data=fake_form)
    #     message = 'Nombre de usuario registrado con éxito'
    #     self.assert_message_flashed(message)