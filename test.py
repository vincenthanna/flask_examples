import os
import flask
import flaskr
import unittest
import tempfile



class flaskrTestCase(unittest.TestCase):

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()
        print("aaa")

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        strdata = rv.data.decode('utf-8')
        assert 'No entries here so far' in strdata

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data.decode('utf-8')
        rv = self.logout()
        assert 'You were logged out' in rv.data.decode('utf-8')
        rv = self.login('adminx', 'default')
        assert 'Invalid Username' in rv.data.decode('utf-8')
        rv = self.login('admin', 'defaultx')
        assert 'Invalid Password' in rv.data.decode('utf-8')

    def test_message(self):
        print(">>>>>>>>> test_message")
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(title='<Hello>', text='<strong>HTML</strong> allowed here'), follow_redirects=True)
        assert 'No entries here so far' not in rv.data.decode('utf-8')
        assert '&lt;Hello&gt;' in rv.data.decode('utf-8')
        assert '<strong>HTML</strong> allowed here' in rv.data.decode('utf-8')


if __name__ == '__main__':
    unittest.main()

