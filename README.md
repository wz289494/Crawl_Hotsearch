一、概述
这是一个用于获取各平台热搜榜单的爬虫项目，可获取社交媒体（微博、抖音热榜等）、商品（淘宝、天猫热卖榜等）
今日热榜:https://tophub.today

二、依赖
详见requirements.txt
终端安装:pip install -r requirements.txt

三、模块介绍
1、crawl模块主要存储爬取配置，以及提供爬取模式，根据网页不同的模块，有不同的模式可以选择
详细查看:help(Crawl)
2、extract模块主要存储数据解析函数
详细查看:help(Extract)
3、store模块主要存储数据保存函数，包含mysql存储以及excel存储
详细查看:help(Store)
4、main模块为项目主要流程模块，包含实际业务逻辑，可自行布置
5、test模主要测试爬虫可行性
6、catalog模块主要针对爬取下来的excel文件进行编码，形成Directory文件
Directory文件储存榜单类目信息，主要包含平台+榜单

四、说明
1、crawl中setting设置
打开F12工具，定位json数据或是文档数据，复制curl
打开网页https://curlconverter.com/，获取cookie及headers
2、store中修改mysql的密码.
