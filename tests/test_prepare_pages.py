"""Regression tests for the 3DVista source-to-site path mapping."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.prepare_pages import destination_for


class DestinationForTests(unittest.TestCase):
    def setUp(self):
        self.source = Path('/tmp/3dvista-source')

    def test_accepts_zip_tour_wrapper_for_index(self):
        path = self.source / 'tour/storage.net-fs.com/hosting/2727323/443/index.html'
        self.assertEqual(destination_for(self.source, path), Path('index.html'))

    def test_accepts_zip_tour_wrapper_for_player(self):
        path = self.source / 'tour/lib/tdvplayer.js'
        self.assertEqual(destination_for(self.source, path), Path('lib/tdvplayer.js'))

    def test_accepts_runtime_script_inside_wrapper(self):
        path = self.source / 'tour/script.js'
        self.assertEqual(destination_for(self.source, path), Path('script.js'))

    def test_accepts_recovered_media_overlay(self):
        path = self.source / 'recursos_recuperados/media/panorama_x/f/0/0_0.jpg'
        self.assertEqual(destination_for(self.source, path), Path('media/panorama_x/f/0/0_0.jpg'))

    def test_ignores_unknown_null_file(self):
        path = self.source / 'recursos_recuperados/null'
        self.assertIsNone(destination_for(self.source, path))

    def test_ignores_download_report(self):
        path = self.source / 'recursos_recuperados/reporte_descarga_selectiva.json'
        self.assertIsNone(destination_for(self.source, path))

    def test_ignores_audit_reports(self):
        path = self.source / 'tour/resultado3.txt'
        self.assertIsNone(destination_for(self.source, path))


if __name__ == '__main__':
    unittest.main()
