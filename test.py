import unittest
import requests_mock
from crawl import Crawl

# 测试代码
class TestCrawl(unittest.TestCase):
    """
    TestCrawl is a unit test class designed to test the functionality of the Crawl class.
    It uses the unittest framework and requests_mock to mock HTTP requests.

    Methods:
        setUp(): Sets up the test environment by initializing the Crawl instance.
        test_get_single_info(mock_request): Tests the get_single_info method.
        test_get_category_info(mock_request): Tests the get_category_info method.
        test_get_all_info(mock_request): Tests the get_all_info method.
        test_get_all_info_async(mock_request): Tests the get_all_info_async method.
        test_get_category_info_async(mock_request): Tests the get_category_info_async method.
    """

    def setUp(self):
        """
        Sets up the test environment by initializing the Crawl instance.
        This method is called before every test case.
        """
        self.crawler = Crawl()

    @requests_mock.Mocker()
    def test_get_single_info(self, mock_request):
        """
        Tests the get_single_info method to ensure it correctly fetches a single page's information.

        Args:
            mock_request (requests_mock.Mocker): The mocker object to mock HTTP requests.
        """
        category = 'comprehensive_info'
        page = 0
        mock_url = self.crawler.url_dict[category]
        mock_request.get(mock_url, text='mocked response')

        result = self.crawler.get_single_info(category, page)
        self.assertEqual(result, 'mocked response')
        self.assertEqual(mock_request.call_count, 1)
        self.assertEqual(mock_request.last_request.qs['p'], ['0'])

    @requests_mock.Mocker()
    def test_get_category_info(self, mock_request):
        """
        Tests the get_category_info method to ensure it correctly fetches all pages' information for a category.

        Args:
            mock_request (requests_mock.Mocker): The mocker object to mock HTTP requests.
        """
        category = 'comprehensive_info'
        page_limit = self.crawler.page_dict[category]
        mock_url = self.crawler.url_dict[category]
        mock_request.get(mock_url, text='mocked response')

        result = self.crawler.get_category_info(category)
        self.assertEqual(result, 'mocked response' * page_limit)
        self.assertEqual(mock_request.call_count, page_limit)

    @requests_mock.Mocker()
    def test_get_all_info(self, mock_request):
        """
        Tests the get_all_info method to ensure it correctly fetches all information for all categories.

        Args:
            mock_request (requests_mock.Mocker): The mocker object to mock HTTP requests.
        """
        for category in self.crawler.url_dict:
            mock_url = self.crawler.url_dict[category]
            mock_request.get(mock_url, text='mocked response')

        result = self.crawler.get_all_info()
        expected_result = ''.join(['mocked response' * self.crawler.page_dict[category] for category in self.crawler.page_dict])
        self.assertEqual(result, expected_result)

    @requests_mock.Mocker()
    def test_get_all_info_async(self, mock_request):
        """
        Tests the get_all_info_async method to ensure it correctly fetches all information for all categories asynchronously.

        Args:
            mock_request (requests_mock.Mocker): The mocker object to mock HTTP requests.
        """
        for category in self.crawler.url_dict:
            mock_url = self.crawler.url_dict[category]
            mock_request.get(mock_url, text='mocked response')

        result = self.crawler.get_all_info_async()
        expected_result = ''.join(['mocked response' * self.crawler.page_dict[category] for category in self.crawler.page_dict])
        self.assertEqual(result, expected_result)

    @requests_mock.Mocker()
    def test_get_category_info_async(self, mock_request):
        """
        Tests the get_category_info_async method to ensure it correctly fetches all pages' information for a category asynchronously.

        Args:
            mock_request (requests_mock.Mocker): The mocker object to mock HTTP requests.
        """
        category = 'comprehensive_info'
        page_limit = self.crawler.page_dict[category]
        mock_url = self.crawler.url_dict[category]
        mock_request.get(mock_url, text='mocked response')

        result = self.crawler.get_category_info_async(category)
        self.assertEqual(result, 'mocked response' * page_limit)
        self.assertEqual(mock_request.call_count, page_limit)

if __name__ == '__main__':
    unittest.main()
