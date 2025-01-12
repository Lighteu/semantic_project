from html import unescape
import re


def strip_html_tags(text):
    clean = re.sub(r'<[^>]+>', '', text)  
    return unescape(clean.strip()) 