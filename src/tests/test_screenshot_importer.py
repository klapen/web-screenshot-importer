import random, string, json
from config import app
from unittest import TestCase, main, mock
from resources.ScreenshotImporter import ScreenshotImporter

def random_string_generator(size):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

class TestScreenshotImporter(TestCase):
    def setUp(self):
        self.importer = ScreenshotImporter

    @mock.patch("resources.ScreenshotImporter.Log")
    @mock.patch("resources.ScreenshotImporter.db")
    def test_invalid_db_status(self, mock_db, mock_log):
        mock_value = {
            'url': random_string_generator(32),
            'status': random_string_generator(32),
            'image_url': random_string_generator(32)
        }

        res = self.importer._saveInLog(self.importer, mock_value['url'], mock_value['status'], mock_value['image_url'])
        self.assertFalse(mock_log.called, 'Should not create a log db item')
        self.assertFalse(mock_db.session.add.called, 'Should not add to save on database')
        self.assertFalse(mock_db.session.commit.called, 'Should not commit changes to DB')
        self.assertFalse(res, 'Should return false on fail')

    @mock.patch("resources.ScreenshotImporter.Log")
    @mock.patch("resources.ScreenshotImporter.db")
    def test_exception_saving_on_db(self, mock_db, mock_log):
        mock_value = {
            'url': random_string_generator(32),
            'status': 'failed',
            'image_url': random_string_generator(32)
        }

        mock_log.return_value = mock_value
        mock_db.session.commit.side_effect = Exception('Error on DB')
        
        res = self.importer._saveInLog(self.importer, mock_value['url'], mock_value['status'], mock_value['image_url'])
        mock_db.session.add.assert_called_with(mock_value)
        self.assertTrue(mock_db.session.commit.called, 'Should commit changes to DB')
        self.assertFalse(res, 'Should return false on fail')

    @mock.patch("resources.ScreenshotImporter.Log")
    @mock.patch("resources.ScreenshotImporter.db")
    def test_save_to_db(self, mock_db, mock_log):
        for status in ['sucessfull', 'failed']:
            mock_value = {
                'url': random_string_generator(32),
                'status': status,
                'image_url': random_string_generator(32)
            }
            
            mock_log.return_value = mock_value
            
            res = self.importer._saveInLog(self.importer, mock_value['url'], mock_value['status'], mock_value['image_url'])
            mock_db.session.add.assert_called_with(mock_value)
            self.assertTrue(mock_db.session.commit.called, 'Should commit changes to DB')
            self.assertTrue(res, 'Should return true when sucessful')

    @mock.patch("resources.ScreenshotImporter.db")
    def test_empty_url(self, mock_db):
        res = self.importer.importScreenshot(self.importer, '')
        self.assertEqual(res[1], 400, 'Should respond an 400 error')
        self.assertEqual(res[0], { 'error': 'URL cannot be blank' }, 'Should respond an message text')
        self.assertFalse(mock_db.session.add.called, 'Should not save on DB')
        self.assertFalse(mock_db.session.commit.called, 'Should not commit to DB')
        
    @mock.patch("resources.ScreenshotImporter.db")
    def test_invalid_url(self, mock_db):
        invalid_urls = ['www.google.com', 'google.com', 'google', 'https://google', 'https://.com', 'htps://www.google.com']
        for url in invalid_urls:
            res = self.importer.importScreenshot(self.importer, url)
            self.assertEqual(res[1], 400, 'Should respond an 400 error')
            self.assertEqual(res[0], { 'error': 'Not valid URL' }, 'Should respond an message text')
            self.assertFalse(mock_db.session.add.called, 'Should not save on DB')
            self.assertFalse(mock_db.session.commit.called, 'Should not commit to DB')

    @mock.patch("resources.ScreenshotImporter.requests")
    @mock.patch("resources.ScreenshotImporter.db")
    def test_return_image(self, mock_db, mock_requests):
        with app.app_context():
            api_url = 'https://image.thum.io/get/'
            url = 'https://www.google.com'
            image_mock = random_string_generator(100)
            
            mock_response = mock_requests.Response();
            mock_response.status_code = 200
            mock_response.headers['thum_status_code'] = 200
            mock_response.content = image_mock
            mock_requests.get.return_value = mock_response
            
            res = self.importer.importScreenshot(self, url)
            self.assertEqual(res.data.decode('utf-8'), image_mock, 'Should send a proper image')
            self.assertEqual(res.status_code, 200, 'Should response 200 code')
            self.assertEqual(res.headers.get('Content-Type'), 'image/png', 'Content-Type should be image/png')
            mock_requests.get.assert_called_with(api_url + url)

if __name__ == '__main__':
    main()
