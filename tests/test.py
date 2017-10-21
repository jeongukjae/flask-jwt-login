# -*- coding: utf8 -*-
import unittest
from app import app

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.flask_app = app
        self.app = self.flask_app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        # login id and password
        id = 'idtest1'
        pw = 'pwtest1'

        # try to login
        rv = self.app.post('/login', data={
            'id' : id,
            'pw' : pw
        })

        # result
        assert 'GO!' in rv.data.decode('utf8')
        # check there is a sign in token in response header
        assert 'token=' in rv.headers['Set-Cookie']

    def test_login_failed(self):
        id = 'idtest1'
        pw = 'pw'

        rv = self.app.post('/login', data={
            'id' : id,
            'pw' : pw
        })

        # result
        assert 'Error!' in rv.data.decode('utf8')

    def test_protected(self):
        # test token
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6ImlkdGVzdDEiLCJwdyI6InB3dGVzdDEiLCJuYW1lIjoibmFtZXRlc3QxIn0._Zo-M9TPOJzzvp0paGR7_19_L-492UXAO6MenQr3PfGW5N0QYWPxv7hJK1uav25fDv1hybfJ0-sO_swfhVBd9w'

        # check protected page
        rv = self.app.get('/protected', headers={
            'Cookie': 'token={0}'.format(token)
        })

        assert 'Protected Page' in rv.data.decode('utf8')

    def test_protected_failed(self):
        # check protected page with fake_token
        rv = self.app.get('/protected', headers={
            'Cookie': 'token=fake_token'
        })

        # unauthorized access
        assert rv.status_code == 501

        # check protected page with empty token
        rv = self.app.get('/protected', headers={
        })

        # unauthorized access
        assert rv.status_code == 501

if __name__ == '__main__':
    unittest.main()
