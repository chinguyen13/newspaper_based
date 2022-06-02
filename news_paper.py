import requests
import unicodedata
import re
from datetime import datetime
# result = requests.get('https://edition.cnn.com/2022/05/31/asia/china-taiwan-invasion-scenarios-analysis-intl-hnk-ml/index.html')

# raw = result.text

# with open("raw.txt", "w", encoding="utf-8") as file:
# 	file.write(raw)


def read_url(url):
    result = requests.get(url)
    raw_data = result.text
    if "cnn.com" in url:
        host = "cnn"
    else:
        host = "other"
    return {"raw_data": raw_data, "host": host}


def get_body(raw_data):
    begin = raw_data['raw_data'].find("<body")
    end = raw_data['raw_data'].find("</body>")
    raw_data['raw_data'] = raw_data["raw_data"][begin:end+7]
    raw = raw_data['raw_data'].split("><")
    data = ""
    for i in range(len(raw)):
        raw[i] = "<" + raw[i] + ">"
        if "<script" not in raw[i]:
        	data += raw[i]
    raw_data["raw_data"] = data
    return raw_data


def get_title(raw_data):
    begin = raw_data['raw_data'].rfind("<h1")
    end = raw_data['raw_data'].rfind("</h1>")

    if(begin > 0 and end > 0):
        title = raw_data['raw_data'][begin:end]
        if "title" in title or "head" in title:
	        end_tag = title.find('>')
	        title = title[end_tag+1:]
	        title = unicodedata.normalize("NFKD", title)
        	return title

        else:
        	return "Not found!"
    else:
        return "Not found!"


def get_content(raw_data):
    if raw_data['host'] == "cnn":
        begin = raw_data['raw_data'].find(
            '<section class=\"zn zn-body-text zn-body')
        end = raw_data['raw_data'][begin:].find("</section>")

        article = raw_data['raw_data'][begin:][:end]
        data = article.split("><")
        for i in range(len(data)):
            data[i] = "<" + data[i] + ">"
        read = []
        for line in data:
            if "zn-body__paragraph" in line or "el-editorial-source" in line or "<h3>" in line:
                tags = []
                for i in range(len(line)):
                    if line[i] == "<":
                        begin = i
                    if line[i] == ">":
                        end = i
                        tags.append(line[begin:end+1])
                for tag in tags:
                    line = line.replace(tag, "")

                read.append(line)
        read = list(filter(None, read))
        news = "\n".join(read)
        news = unicodedata.normalize("NFKD", news)
        return news

    else:
        begin = raw_data['raw_data'].find('<article')
        end = raw_data['raw_data'][begin:].find("</article>")

        article = raw_data['raw_data'][begin:][:end]

        data = article.split("><")
        for i in range(len(data)):
            data[i] = "<" + data[i] + ">"
        read = []
        for line in data:
            if "<p" in line and "</p" in line:
                tags = []
                for i in range(len(line)):
	                if line[i] == "<":
	                    begin = i
	                if line[i] == ">":
	                    end = i
	                    tags.append(line[begin:end+1])
                for tag in tags:
	                line = line.replace(tag, "")
                line = line.strip()
                read.append(line)
        news = "\n".join(read)
        news = unicodedata.normalize("NFKD", news)
        return news


def get_date(raw_data):
	try:
	    data = raw_data['raw_data']

	    match_str1 = re.search(r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})[,]\s+(\d{4})", data)

	    match_str2 = re.search(r'((\d{1,2})+/(\d{1,2})+/(\d{4}))', data)
	    if match_str1 != None:
	    	res = match_str1[0]
	    elif match_str2 != None:
	    	res = datetime.strptime(match_str2.group(), '%d/%m/%Y').date()
	    else:
	    	res = "Not Found"
	  
	    return res
	except:
		return "Not Found"


def get_author(raw_data):
	data = raw_data['raw_data'].split("><")
	for line in data:
		if "author" in line and ("by" in line or "By" in line):
			begin = line.find(">")
			end = line.find("</")
			author = line[begin+1:end]
			if len(author) < 100:
				return author

	return "Not found!"








# CNN News URL link
# https://edition.cnn.com/2022/05/31/asia/china-taiwan-invasion-scenarios-analysis-intl-hnk-ml/index.html
# https://edition.cnn.com/2022/06/01/americas/cuba-us-flights-intl/index.html
# https://edition.cnn.com/2022/05/31/asia/asia-meth-crime-synthetic-drugs-hnk-intl/index.html

# NBC News URL link
# https://www.nbcnews.com/news/us-news/multiple-victims-shooting-tulsa-hospital-gunman-police-say-rcna31551
# https://www.nbcnews.com/pop-culture/pop-culture-news/johnny-depp-amber-heard-trial-verdict-rcna30926

# VNExpress URL Link
# https://vnexpress.net/truong-doan-thai-lan-gap-viet-nam-giong-nhu-chung-ket-4470987.html
# https://vnexpress.net/tat-ca-doanh-nghiep-nguoi-dan-dung-hoa-don-dien-tu-tu-1-7-4470881.html

# Others
# https://www.ndtv.com/india-news/request-pm-arrest-all-of-us-together-arvind-kejriwal-defends-delhi-ministers-over-corruption-charges-3031254#pfrom=home-ndtv_topscroll


url = 'https://edition.cnn.com/2022/05/31/asia/asia-meth-crime-synthetic-drugs-hnk-intl/index.html'

raw_data = read_url(url)

raw_data = get_body(raw_data)

title = get_title(raw_data)

content = get_content(raw_data)

date = get_date(raw_data)

author = get_author(raw_data)

print("Title: " + title)

print("Author: " + author)

print("Date: " + str(date))


print("Article:\n" + content)





# with open("cleaning.txt", "w", encoding="utf-8") as file:
#     file.write(raw_data)
