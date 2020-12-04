import unittest
from collectors.hash_collector import HashCollector


class TestsLoadData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._collector = HashCollector(path="assets/with_data.json")

    def test_empty_json_load(self):
        empty_file_path = "assets/empty_json_file.json"
        data = load_json_file(empty_file_path)
        self.assertEqual('', data)

    def test_json_load_with_data(self):
        collector = HashCollector(path="assets/with_data.json")
        collector.load_from_json()
        self.assertTrue(True)


class TestAppendData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
