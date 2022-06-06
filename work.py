import newspaperBased as news

# URL LINK ---------------------

# https://edition.cnn.com/2022/06/02/europe/putin-ukraine-invasion-100-days-analysis-intl-cmd/index.html
# https://www.nbcnews.com/news/us-news/multiple-people-injured-shooting-wisconsin-cemetery-funeral-rcna31737
# https://vnexpress.net/hlv-gong-cau-thu-viet-nam-thi-dau-nhu-nhung-chien-binh-4471422.html
# https://m.docbao.vn/phap-luat/vu-tinh-that-bong-lai-bi-can-le-tung-van-khai-gi-tintuc826115
# https://dantri.com.vn/the-thao/bao-thai-lan-thua-nhan-thuc-te-phu-phang-khi-doi-dau-voi-u23-viet-nam-20220603132833908.htm
# https://tuoitre.vn/viet-nam-co-the-nhap-xang-malaysia-gia-13000-dong-lit-co-giup-binh-on-gia-xang-dau-20220603124213153.htm


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