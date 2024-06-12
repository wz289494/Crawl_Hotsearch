import requests
import concurrent.futures
import threading

class Crawl(object):
    """
    Crawl is a web scraping class designed to fetch information from different categories of news websites.
    It supports both synchronous and asynchronous scraping methods.
    """


    def __init__(self):
        """
        Initializes the Crawl class with cookies, headers, and parameters required for the HTTP requests.
        It also sets up dictionaries for page limits and URLs for different categories.
        """
        self.cookies = {
            'Hm_lvt_3b1e939f6e789219d8629de8a519eab9': '1715853553,1715855472,1715858860',
            'Hm_lpvt_3b1e939f6e789219d8629de8a519eab9': '1715859056',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'priority': 'u=1, i',
            'referer': 'https://tophub.today/c/news',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.params = {
            'p': '',
        }

        self.page_dict = {
            'comprehensive_info': 31,
            'technological_info': 25,
            'recreational_info': 29,
            'communal_info': 23,
            'shop_info': 11,
            'financial_info': 14,
            'newspaper_info': 10
        }

        self.url_dict = {
            'comprehensive_info': 'https://tophub.today/c/news',
            'technological_info': 'https://tophub.today/c/tech',
            'recreational_info': 'https://tophub.today/c/ent',
            'communal_info': 'https://tophub.today/c/community',
            'shop_info': 'https://tophub.today/c/shopping',
            'financial_info': 'https://tophub.today/c/finance',
            'newspaper_info': 'https://tophub.today/c/epaper'
        }

        self.lock = threading.Lock()

    def get_all_info(self):
        """
        Synchronously fetches all information from all categories.

        Returns:
            str: Concatenated string of all fetched information.
        """
        print("Starting synchronous fetching of all information...")
        all_info = ''
        for category in self.page_dict:
            print(f"Fetching information for category: {category}")
            all_info += self.get_category_info(category)
        print("Completed synchronous fetching of all information.")
        return all_info

    def get_category_info(self, category):
        """
        Synchronously fetches information for a specific category.

        Args:
            category (str): The category of information to fetch.

        Returns:
            str: Concatenated string of fetched information for the category.
        """
        if category not in self.page_dict or category not in self.url_dict:
            return "Invalid category"

        print(f"Starting synchronous fetching for category: {category}")
        all_page_str = ''
        for page_num in range(self.page_dict[category]):
            all_page_str += self.get_single_info(category, page_num)
        print(f"Completed synchronous fetching for category: {category}")
        return all_page_str

    def get_single_info(self, category, page):
        """
        Fetches information for a specific page in a category.

        Args:
            category (str): The category of information to fetch.
            page (int): The page number to fetch.

        Returns:
            str: The fetched information as a string.
        """
        self.params['p'] = str(page)
        response = requests.get(self.url_dict[category], params=self.params, cookies=self.cookies, headers=self.headers)
        print(f"Fetched page {page} for category {category}")
        return response.text

    def get_all_info_async(self):
        """
        Asynchronously fetches all information from all categories.

        Returns:
            str: Concatenated string of all fetched information.
        """
        print("Starting asynchronous fetching of all information...")
        all_info = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.get_category_info_async, category): category for category in self.page_dict}
            for future in concurrent.futures.as_completed(futures):
                category = futures[future]
                try:
                    result = future.result()
                    with self.lock:
                        all_info += result
                except Exception as exc:
                    with self.lock:
                        all_info += f"\n{category} generated an exception: {exc}"
        print("Completed asynchronous fetching of all information.")
        return all_info

    def get_category_info_async(self, category):
        """
        Asynchronously fetches information for a specific category.

        Args:
            category (str): The category of information to fetch.

        Returns:
            str: Concatenated string of fetched information for the category.
        """
        if category not in self.page_dict or category not in self.url_dict:
            return "Invalid category"

        print(f"Starting asynchronous fetching for category: {category}")
        all_page_str = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.get_single_info, category, page_num): page_num for page_num in
                       range(self.page_dict[category])}
            for future in concurrent.futures.as_completed(futures):
                page_num = futures[future]
                try:
                    result = future.result()
                    with self.lock:
                        all_page_str += result
                except Exception as exc:
                    with self.lock:
                        all_page_str += f"\nPage {page_num} generated an exception: {exc}"
        print(f"Completed asynchronous fetching for category: {category}")
        return all_page_str

if __name__ == '__main__':
    # a = Crawl()
    # a.get_single_info()

    help(Crawl)