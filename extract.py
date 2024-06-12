from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class Extract(object):
    """
        Extract is a web scraping class designed to extract and process information
        from HTML text. The class provides methods to extract relevant details such as
        titles, links, hot counts, platforms, lists, and recorded times from specific
        HTML elements. The recorded times are converted to a standard datetime format.

        Methods:
            extract_info(text): Extracts information from the given HTML text and returns
                                a list of dictionaries containing the extracted details.
            safe_find_text(parent, tag, class_name): Safely finds and returns the text of a tag
                                within a parent element. Returns an empty string if the tag is not found.
            extract_link(element): Extracts the href link from an element.
            __cal_time(past_time): Calculates the datetime object from a relative time string.
    """

    def extract_info(self, text):
        """
        Extracts information from the given HTML text.

        Args:
            text (str): HTML text to parse.

        Returns:
            list: A list of dictionaries containing extracted information.
        """
        soup = BeautifulSoup(text, 'html.parser')
        item_list = []

        first_items = soup.find_all('div', class_='cc-cd')

        for fir_item in first_items:
            platform = self.__find_text(fir_item, 'div', 'cc-cd-lb')
            slist = self.__find_text(fir_item, 'span', 'cc-cd-sb-st')
            time_text = self.__find_text(fir_item, 'div', 'i-h')
            rectime = self.__cal_time(time_text) if time_text else None

            sec_items = fir_item.find_all('a', target="_blank")
            for sec_item in sec_items:
                # print(sec_item)

                title = self.__find_text(sec_item, 'span', 't')
                if title == '':
                    title = self.__find_text(sec_item, 'div', 'tt')

                hotcount = self.__find_text(sec_item, 'span', 'e')
                if hotcount is None:
                    hotcount = self.__find_text(sec_item, 'div', 'ss')

                item_dict = {
                    'title': title if title else '',
                    'link': self.__extract_link(sec_item),
                    'hotcount': hotcount if hotcount else '',
                    'platform': platform if platform else '',
                    'slist': slist if slist else '',
                    'rectime': rectime.strftime('%Y-%m-%d %H:%M:%S') if rectime else ''
                }
                item_list.append(item_dict)

        return item_list

    def __find_text(self, parent, tag, class_name):
        """
        Safely finds and returns the text of a tag within a parent element.
        Returns an empty string if the tag is not found.

        Args:
            parent (Tag): The parent element to search within.
            tag (str): The tag name to search for.
            class_name (str): The class name to match.

        Returns:
            str: The text content of the tag or an empty string if not found.
        """
        try:
            element = parent.find(tag, class_=class_name)
            return element.text.strip() if element else ''
        except:
            return ''

    def __extract_link(self, element):
        """
        Extracts the href link from an element.

        Args:
            element (Tag): The element to extract the link from.

        Returns:
            str: The extracted link or an empty string if not found.
        """
        link = element.get('href')
        return f'https://tophub.today{link}' if link else ''

    def __cal_time(self, past_time):
        """
        Calculates the datetime object from a relative time string.

        Args:
            past_time (str): The relative time string.

        Returns:
            datetime: The calculated datetime object.
        """
        now = datetime.now()
        past_time = past_time.strip()

        if past_time.endswith("前"):
            time_units = {
                '小时': 'hours',
                '分钟': 'minutes',
                '天': 'days',
                '秒': 'seconds'
            }
            for unit, kwarg in time_units.items():
                if unit in past_time:
                    time_diff = int(past_time.split(unit)[0].strip())
                    past_time_obj = now - timedelta(**{kwarg: time_diff})
                    break
            else:
                raise ValueError("无法识别的时间单位")
        else:
            try:
                past_time_obj = datetime.strptime(past_time, '%Y-%m-%d')
                past_time_obj = past_time_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            except ValueError:
                raise ValueError("无效的时间格式")

        return past_time_obj.replace(microsecond=0)

# 使用示例
if __name__ == "__main__":
    # 示例 HTML 文本
    html_text = '''
    <div class="cc-cd">
        <div class="cc-cd-lb">Platform</div>
        <span class="cc-cd-sb-st">List</span>
        <div class="i-h">5分钟前</div>
        <a target="_blank" href="/link1">
            <span class="t">Title 1</span>
            <span class="e">100</span>
        </a>
        <a target="_blank" href="/link2">
            <span class="t">Title 2</span>
            <span class="e">200</span>
        </a>
    </div>
    '''

    extractor = Extract()
    result = extractor.extract_info(html_text)
    print(result)
    for item in result:
        print(item)
