# encoding: utf-8

import sys
import re
import mechanize
from HTMLParser import HTMLParser
from pit import Pit

class TestHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_title_tag = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title_tag = True

    def handle_data(self, data):
        if self.in_title_tag == True:
            s = 'Result: ' + data
            print conv_encoding(s, 'utf8', sys.stdout.encoding)
            self.in_title_tag = False

def conv_encoding(s, fr, to):
    s = s.decode(fr)
    s = s.encode(to)
    return s

def main(text):
    url = Pit.get('nikki', {'require': {'url': 'form url'}})['url']

    agent = mechanize.Browser()
    agent.set_handle_robots(False)
    agent.open(url)
    agent.select_form(nr=0)
    agent['entry.0.single'] = text
    response = agent.submit()
    html = response.read()

    parser = TestHTMLParser()
    parser.feed(html)
    parser.close()

if __name__ == '__main__':
    vals =sys.argv
    vals.remove(vals[0])
    text = ' '.join(vals)

    s = conv_encoding(text, sys.stdin.encoding, 'utf8')
    main(s)

