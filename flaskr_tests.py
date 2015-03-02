import os,flaskr,unittest,tempfile




class FlaskTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		flaskr.app.config['TESTING'] = True
		self.app = flaskr.app.test_client()
		flaskr.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_empty_db(self):
		r = self.app.get('/')
		assert 'not content' in r.data

'''
	def test_login_logout(self):
		rv = self.login('admin', 'default')
		assert 'login sucessful' in rv.data
'''





if __name__ == '__main__':
	unittest.main()