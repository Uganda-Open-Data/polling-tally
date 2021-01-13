from django.test import TestCase
from django.contrib.auth.models import User


class CredsTestCate(TestCase):
    def test_root_url_is_login(self):
        r = self.client.get('/')
        page_content = r.content.decode('utf8')
        self.assertEquals(r.status_code, 200)
        self.assertTemplateUsed('login.html')
        self.assertInHTML('<title>Login</title>', page_content)

    def test_sign_up_page_uses_correct_template(self):
        r = self.client.get('/signup')
        page_content = r.content.decode('utf8')
        self.assertEquals(r.status_code, 200)
        self.assertTemplateUsed('signup.html')
        self.assertInHTML('<title>Signup</title>', page_content)

    def test_sign_up_page_creates_user_and_redirects_to_login(self):
        r = self.client.post(
            '/signup', data={
                'email': 'john.doe@example.com',
                'username': 'johndoe',
                'password1': 'lgBGASI43@#',
                'password2': 'lgBGASI43@#'
            }
        )
        user_exists = User.objects.filter(email='john.doe@example.com').exists()
        self.assertEquals(r.status_code, 200)
        self.assertTemplateUsed('login.html')
        self.assertTrue(user_exists)

    def test_login_page_uses_correct_template(self):
        r = self.client.get('/login')
        page_content = r.content.decode('utf8')
        self.assertEquals(r.status_code, 200)
        self.assertTemplateUsed('login.html')
        self.assertInHTML('<title>Logi</title>', page_content)

    
    def test_reset_password_page_setup(self):
        r = self.client.get('/reset-password')
        page_content = r.content.decode('utf8')
        self.assertEquals(r.status_code, 200)
        self.assertTemplateUsed('reset-password.html')
        self.assertInHTML('<title>Reset Password</title>', page_content)
