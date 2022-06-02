import requests
import unicodedata
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

    header_position = raw_data['raw_data'].find("</header>")
    if begin > 0 and end > 0:
    	raw_data["raw_data"] = raw_data["raw_data"][header_position:]
    return raw_data


def get_title(raw_data):
    begin = raw_data['raw_data'].find("<h1")
    end = raw_data['raw_data'].find("</h1>")
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
                read.append(line)
        news = "\n".join(read)
        news = unicodedata.normalize("NFKD", news)
        return news


def get_time(raw_data):
    data = raw_data['raw_data'].split("><")
    data_list = []
    for i in range(len(data)):
        if "time" in data[i] or "date" in data[i]:
            data[i] = "<" + data[i] + ">"
            tags = []
            for j in range(len(data[i])):
                if data[i][j] == "<":
                    begin = j
                if data[i][j] == ">":
                    end = j
                    tags.append(data[i][begin:end+1])
            for tag in tags:
                data[i] = data[i].replace(tag, "")
            data_list.append(data[i])
    # datetime = list(filter(None, data_list))
    print(data_list)
  










url = 'https://vnexpress.net/tat-ca-doanh-nghiep-nguoi-dan-dung-hoa-don-dien-tu-tu-1-7-4470881.html'

# CNN News URL link
# https://edition.cnn.com/2022/05/31/asia/china-taiwan-invasion-scenarios-analysis-intl-hnk-ml/index.html
# https://edition.cnn.com/2022/06/01/americas/cuba-us-flights-intl/index.html
# https://edition.cnn.com/2022/05/31/asia/asia-meth-crime-synthetic-drugs-hnk-intl/index.html

# NBC News URL link
# https://www.nbcnews.com/news/us-news/multiple-victims-shooting-tulsa-hospital-gunman-police-say-rcna31551
# https://www.nbcnews.com/pop-culture/pop-culture-news/johnny-depp-amber-heard-trial-verdict-rcna30926

# The Guardian URL link
# https://www.theguardian.com/uk-news/2022/may/31/first-rwanda-deportation-flight-leave-uk-14-june-priti-patel
# https://www.theguardian.com/sport/2022/jun/01/cilic-defeats-rublev-in-five-sets-to-reach-french-open-last-four-for-first-time

# VNExpress URL Link
# https://vnexpress.net/truong-doan-thai-lan-gap-viet-nam-giong-nhu-chung-ket-4470987.html
# https://vnexpress.net/tat-ca-doanh-nghiep-nguoi-dan-dung-hoa-don-dien-tu-tu-1-7-4470881.html

raw_data = read_url(url)

raw_data = get_body(raw_data)

title = get_title(raw_data)

content = get_content(raw_data)
get_content(raw_data)

print(title)

print()

print(content)

# print(get_time(raw_data))

# with open("cleaning.txt", "w", encoding="utf-8") as file:
#     file.write(raw_data)
