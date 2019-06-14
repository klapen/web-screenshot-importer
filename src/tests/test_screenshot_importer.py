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
            mock_requests.get.assert_called_with(api_url + url)

if __name__ == '__main__':
    main()
