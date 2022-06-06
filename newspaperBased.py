import requests
import re
from datetime import datetime
import TF_IDF 

def Article(url):
    result = requests.get(url)
    return result


def get_html(article):
    raw = article.text
    return raw

def parse(article):
    raw = article.text
    #  Split each line based on end tag
    raw = raw.replace("\n","")

    raw = raw.split("><")
    raw[0] += ">"
    raw[-1] = "<" + raw[-1]
    for i in range(1, len(raw)-1):
        raw[i] = "<" + raw[i] + ">"

    # Select only in <Body> tag
    try:
        for i in range(len(raw)):
            if "<body" in raw[i]:
                begin = i
            if "</body>" in raw[i]:
                raw = raw[begin:i+1]
                break
    except Exception:
        pass

    # Remove <script> line
    for i in range(len(raw)):
        if "<script" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    # Remove video line
    for i in range(len(raw)):
        if "videoUrl" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    # Remove <style> line
    for i in range(len(raw)):
        if "<style" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    # Remove <!-- --> line
    for i in range(len(raw)):
        if "<!--" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    # Remove /* */ line
    for i in range(len(raw)):
        if "/*" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    return raw


def get_content(raw):    

    title = get_title(raw)
    for i in range(len(raw)):
        if "caption" in raw[i] or "Photograph" in raw[i]:
            raw[i] = ""
    raw = list(filter(None, raw))

    for i in range(len(raw)):
    	tags = []
    	for j in range(len(raw[i])):
    		if raw[i][j] == "<":
    			begin = j
    		if raw[i][j] == ">":
    			tags.append(raw[i][begin:j+1])
    	for tag in tags:
    		raw[i] = raw[i].replace(tag , "")
    		continue
    raw = list(filter(None, raw))

    # Remove unnecessary extra space
    for i in range(len(raw)):
        raw[i] = " ".join(raw[i].strip().split())
    raw = list(filter(None, raw))

    # Content
    begin = -1
    content = []
    for i in range(len(raw)):
        if begin > 0:
            if len(raw[i]) >= 90:
                content.append(raw[i])
        if title in raw[i]:
        	begin = i

    return "\n".join(content)



def get_title(data):
    titles = []
    for i in range(len(data)):
        if "<h1" in data[i]:
            titles.append(data[i])
            
    if len(titles) == 0:
    	return "Not Found"
    for i in range(len(titles)):
        if "img" not in titles[i]:
            begin = titles[i].find("<h1")

            titles[i] = titles[i][begin:]
            end = titles[i].find("</h1>")
            if end != -1:
            	titles[i] = titles[i][:end]
            tags = []
            for j in range(len(titles[i])):
                if titles[i][j] == "<":
                    begin = j
                if titles[i][j] == ">":
                    tags.append(titles[i][begin:j+1])
            for tag in tags:
                titles[i] = titles[i].replace(tag, "")
            titles[i] = titles[i].strip()
            if len(titles[i]) > 20:
            	return titles[i]
    return "Not Found"


def get_date(data):
    for line in data:
        match_str1 = re.search(
            r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})[,]\s+(\d{4})", line)
        match_str2 = re.search(
            r'([0]?[1-9]|[1|2][0-9]|[3][0|1])[/]([0]?[1-9]|[1][0-2])[/]([0-9]{4})', line)

        if match_str1 != None:
            res = match_str1[0]
            return res
        elif match_str2 != None:
            try:
                res = datetime.strptime(match_str2.group(), '%d/%m/%Y').date()
                return res
            except Exception:
                continue
    return "Not Found"

def get_author(data):
    raw = []
    for line in data:
        if "author" in line:
            raw.append(line)
    if len(raw) == 0:
        return "Not Found!"
    tags = []
    for i in range(len(raw)):
        for j in range(len(raw[i])):
            if raw[i][j] == "<":
                begin = j
            if raw[i][j] == ">":
                tags.append(raw[i][begin:j+1])
        for tag in tags:
            raw[i] = raw[i].replace(tag,"")
        raw[i] = raw[i].strip()
        if len(raw[i]) > 0:
            return raw[i]
    return "Not Found!"

def get_summary(data):
    try:
        summary = TF_IDF.summary(data)
    except Exception:
        summary = "Error while summarizing!"
    return summary


