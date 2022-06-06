import newspaperBased as news

# URL LINK ---------------------

# https://edition.cnn.com/2022/06/02/europe/putin-ukraine-invasion-100-days-analysis-intl-cmd/index.html
# https://www.nbcnews.com/news/us-news/multiple-people-injured-shooting-wisconsin-cemetery-funeral-rcna31737
# https://vnexpress.net/hlv-gong-cau-thu-viet-nam-thi-dau-nhu-nhung-chien-binh-4471422.html
# https://m.docbao.vn/phap-luat/vu-tinh-that-bong-lai-bi-can-le-tung-van-khai-gi-tintuc826115
# https://www.theguardian.com/world/2022/jun/06/south-korea-and-us-fire-eight-missiles-into-sea-in-show-of-force-to-north-korea
# https://news.yahoo.com/kharkiv-region-russians-defending-themselves-153723401.html?guccounter=1&guce_referrer=aHR0cHM6Ly9uZXdzLmdvb2dsZS5jb20v&guce_referrer_sig=AQAAAHP15kXl4_YuvJ7EZrZAHI0RHTRtUEeFhpxmBAUOOROQUCpYScqGJK5LqLzj8U7FFfWfK9mpPDA1wkPUavRTyu9GpCGy-OVu5ZXdA1d1rvmkRKsgGuh-MV7AXAIOEHO81XdhBl5FZbq3gucvr0G99mEp3u4zytDGDWVNEKawJcNz
# https://www.cnbc.com/2022/06/05/beijing-to-allow-indoor-dining-further-easing-covid-curbs.html
# https://www.reuters.com/business/energy/exclusive-us-let-eni-repsol-ship-venezuela-oil-europe-debt-sources-2022-06-05/
# https://www.theverge.com/2022/6/5/23149921/apple-wwdc-2022-news-rumors-products-announcements
# https://www.tomsguide.com/opinion/iphone-14-apple-please-dont-overcomplicate-the-always-on-display

url = 'https://edition.cnn.com/2022/06/02/europe/putin-ukraine-invasion-100-days-analysis-intl-cmd/index.html'

article = news.Article(url)

html = news.get_html(article)

data = news.parse(article)

title = news.get_title(data)

date = news.get_date(data)

author = news.get_author(data)

content = news.get_content(data)

summary = news.get_summary(content)

print("Title: " + title)

print("\nDate: " + str(date))

print("\nAuthor: " + author)

print("\nContent: \n" + content)

print("\n\nSummary: \n" + summary)