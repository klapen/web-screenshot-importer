from unittest import TestCase, main, mock
from src.resources.ScreenshotImporter import ScreenshotImporter

class TestScreenshotImporter(TestCase):
    def setUp(self):
        self.importer = ScreenshotImporter

    @mock.patch("src.resources.ScreenshotImporter.db")
    def test_invalid_url(self, mock_db):
        invalid_urls = ['www.google.com', 'google.com', 'google', 'https://google', 'https://.com', 'htps://www.google.com']
        for url in invalid_urls:
            res = self.importer.get(self.importer, url)
            self.assertEqual(res[1], 400, 'Should respond an 400 error')
            self.assertEqual(res[0], { 'message': 'Not valid URL' }, 'Should respond an message text')
            self.assertFalse(mock_db.session.add.called, 'Should not save on DB')
            self.assertFalse(mock_db.session.commit.called, 'Should not commit to DB')

if __name__ == '__main__':
    main()
