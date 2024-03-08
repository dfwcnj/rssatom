
import os
import sys
import json
import pprint
import re
import argparse
import urllib.request
import webbrowser

import xml
import xml.etree.ElementTree as ET


class RSSAtom2HTML():

    def __init__(self):
        self.tree = None
        self.root = None
        self.rstr = None
        self.htmla = []

    def processRSSAtomChild(self, root):
        url = None
        width = None
        height = None
        categories=[]
        domains = set()
        for child in root:
            tag = child.tag
            txt = child.text
            if '{' in tag:
                taga = re.split('[{}]', child.tag)
                tag = taga[2]
            if tag == 'title':
                h = '<h3>%s</h3>' % (txt)
                self.htmla.append(h)
            elif tag == 'id':
                h = '<a href="%s">%s</a>' % (txt, tag)
                self.htmla.append(h)
            elif tag == 'guid':
                h = '<a href="%s">%s</a>' % (txt, tag)
                self.htmla.append(h)
            elif tag == 'link':
                if txt:
                    h = '<a href="%s">%s</a>' % (txt, tag)
                    self.htmla.append(h)
            elif tag in ['credit', 'description', 'copyright', 'pubDate',
                         'lastBuildDate', 'updated', 'updatePeriod']:
                h = '<p>%s: %s</p>' % (tag, txt)
                self.htmla.append(h)
            elif tag == 'category':
                categories.append(txt)
            elif tag == 'summary':
                if txt:
                    if '<h4>' in txt:
                        self.htmla.append(txt)
                    else:
                        print('RSSAtomChild tag: %s text: %s' %(tag, txt),
                            file=sys.stderr)
            elif tag == 'content':
                if txt:
                    if '<ol>' in txt or '<a' in txt:
                        self.htmla.append(txt)
                    else:
                        print('RSSAtomChild tag: %s text: %s' %(tag, txt),
                            file=sys.stderr)
            elif tag == 'creator':
                h = '<p>%s: %s</p>' % (tag, txt)
                self.htmla.append(h)
            elif tag == 'name':
                h = '<p>%s</p>' % (txt)
                self.htmla.append(h)
            elif tag == 'email':
                h = '<a href="mailto:%s">%s</a>' % (txt, tag)
                self.htmla.append(h)
            elif tag == 'uri':
                h = '<a href="%s">%s</a>' % (txt, tag)
                self.htmla.append(h)
            elif tag == 'url':
                url = txt
            elif tag == 'width':
                width = txt
            elif tag == 'height':
                height = txt
            elif tag == 'entry':
                pass
            else:
                if url:
                    h = '<img src="%s" width="%s height="%s">' % (url,
                         width, height)
                    self.htmla.append(h)
                else:
                    print('RSSAtomChild tag: %s text: %s' %(tag, txt),
                        file=sys.stderr)
            ad = child.attrib
            aurl = None
            awidth = None
            aheight = None
            for k in ad.keys():
                v = ad[k]
                if k == 'url':
                    aurl = v
                elif k == 'href':
                    h = '<a href="%s">link</a>' % (v)
                    self.htmla.append(h)
                elif k == 'domain':
                    domains.add(v)
                elif k == 'type':
                    pass
                elif k == 'width':
                    awidth = v
                elif k == 'height':
                    aheight = v
                else:
                    print('RSSAtomChild attr: k %s v %s' % (k, v),
                        file=sys.stderr )
                if aurl:
                    h = '<img src="%s" width="%s height="%s">' % (aurl,
                         awidth, aheight)
                    self.htmla.append(h)
            self.processRSSAtomChild(child)
            if len(categories):
                h = '<p>categories: %s</p>' % (','.join(categories))
            if len(domains):
                h = '<p>domains: %s</p>' % (','.join(domains))

    def processRSSAtom(self):
        self.htmla.append('<html>')
        for child in self.root:
            tag = child.tag
            txt = child.text
            h = None
            if '{' in tag:
                taga = re.split('[{}]', child.tag)
                tag = taga[2]
            if tag == 'id':
                h = '<a href="%s">%s</a>' % (txt, tag)
            elif tag == 'link':
                if txt:
                    h = '<a href="%s">%s</a>' % (txt, tag)
            elif tag == 'generator':
                h = '<p>%s: %s</p>' % (tag, txt)
            elif tag == 'title':
                h = '<h1>%s: %s</h1>' % (tag, txt)
            elif tag == 'subtitle':
                h = '<p>%s: %s</p>' % (tag, txt)
            elif tag == 'updated':
                h = '<p>%s: %s</p>' % (tag, txt)
            elif tag == 'rights':
                h = '<p>%s: %s</p>' % (tag, txt)
            elif tag == 'entry':
                pass
            elif tag == 'author':
                pass
            else:
                print('RSSAtom tag: %s text: %s' %(tag, txt), file=sys.stderr)
            if h:
                self.htmla.append(h)
            ad = child.attrib
            for k in ad.keys():
                v = ad[k]
                if k == 'type':
                    pass
                elif k == 'rel':
                    pass
                elif k == 'href':
                    pass
                else:
                    print('RSSAtom attr: k %s v %s' % (k, v),file=sys.stderr )
            self.processRSSAtomChild(child)
        self.htmla.append('</html>')

    def parseRSSAtom(self, rstr):
        self.root = ET.fromstring(rstr)

    def getRSSAtom(self, url):
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req)
        except Exception as e:
            print('getRSSAtom url %s: %s' % (url, e),file=sys.stderr )
            sys.exit(1)
        try:
            self.rstr = resp.read().decode('utf-8')
        except Exception as e:
            print('getRSSAtom %s: %s' % (url, e) )
            sys.exit()
        return self.rstr

    def reportHTML(self):
        return ''.join(self.htmla)

def main():
    argp = argparse.ArgumentParser(description='parse rss or atom file')
    argp.add_argument('--url', required = True,
        help='url of an atom file to parse')
    argp.add_argument('--htmlfile',
        help='where to store the generated output')
    argp.add_argument('--show', action='store_true', default=False,
        help='show the feed in a browser')

    args = argp.parse_args()

    RA = RSSAtom2HTML()
    rstr = RA.getRSSAtom(args.url)
    RA.parseRSSAtom(rstr)
    RA.processRSSAtom()
    html = RA.reportHTML()

    if args.htmlfile:
        with open(args.htmlfile, 'w') as fp:
            fp.write(html)
        if args.show:
            webbrowser.open('file://%s' % (args.htmlfile), new=0 )
    else:
        print(html)

if __name__ == '__main__':
    main()
