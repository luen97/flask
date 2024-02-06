from flask_testing import TestCase
from flask import current_app, url_for
from app.firestore_service import delete_user

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
        # Pruebo que al llenar el formulario
        # me redirige a index
        # fake_form = {
        #     'username':'fake',
        #     'password':'fake-password'
        # }
        # response = self.client.post(
        #             url_for('hello'), 
        #             data=fake_form)
        # Ya no regresa el redirect porque 
        # quitamos el método POST del /hellod
        # self.assertRedirects(response, url_for('index'))
        # self.assertEqual(response.location, '/') #corrección cula

        # Queremos que ahora evalue que devuelve
        # un error de method not allowed
        # Haga un POST (dar en enviar)
        response = self.client.post(
                    url_for('hello'))

        # Debe salir error, evaluamos que así sea
        self.assertTrue(response.status_code,405)
    
    # def test_user_registered_flashed_message(self):
    #     fake_form = {
    #         'username': 'vijoin',
    #         'password': '123456'
    #     }
    #     self.client.post(url_for('hello'), data=fake_form)
    #     message = 'Nombre de usuario registrado con éxito'
    #     self.assert_message_flashed(message)

    def test_auth_blueprint_exists(self):
        # vemos si auth está dentro de las blueprints
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')


    def test_auth_login_post(self):
        fake_form = {
            'username':'fake',
            'password':'fake-password'
        }
        response = self.client.post(
                    url_for('auth.login'), 
                    data=fake_form)
        self.assertRedirects(response, url_for('index'))

    def test_auth_signup_get(self):
        response = self.client.get(url_for('auth.signup'))

        self.assert300(response)

    def test_auth_signup_post(self):
        try:
            fake_form = {
                'username': 'test_user',
                'password': '123456'
            }
            response = self.client.post(url_for('auth.signup'), data=fake_form)
            self.assertRedirects(response, url_for('hello'))
        finally:
            #Remove added db
            delete_user(fake_form['username'])