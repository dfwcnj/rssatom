#! /bin/ksh
set -ex

python src/rssatom/rssatom2html.py \
  --url 'http://news.google.com/atom/' \
  --htmlfile /private/tmp/gn.html

python src/rssatom/rssatom2html.py \
  --url 'http://rss.cnn.com/rss/money_news_international.rss' \
  --htmlfile /private/tmp/cnnmni.html

python src/rssatom/rssatom2html.py \
  --url 'https://feeds.washingtonpost.com/rss/world?itid=lk_inline_manual_35' \
  --htmlfile /private/tmp/wapoworld.html

python src/rssatom/rssatom2html.py \
  --url 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml' \
  --htmlfile /private/tmp/nytworld.html

python src/rssatom/rssatom2html.py \
  --url 'https://www.theregister.com/software/ai_ml/headlines.atom' \
  --htmlfile /private/tmp/traiml.html

python src/rssatom/rssatom2html.py \
  --url 'https://feeds.a.dj.com/rss/RSSWorldNews.xml' \
  --htmlfile /private/tmp/djworld.html

python src/rssatom/rssatom2html.py \
  --url 'https://knowyourmeme.com/newsfeed.rss' \
  --htmlfile /private/tmp/kymnewsfeed.html

python src/rssatom/rssatom2html.py \
  --url 'https://www.sec.gov/news/pressreleases.rss' \
  --htmlfile /private/tmp/secreleases.html

python src/rssatom/rssatom2html.py \
  --url 'https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=2,6,7' \
  --htmlfile /private/tmp/nasdaq.html

python src/rssatom/rssatom2html.py \
  --url 'https://www.treasurydirect.gov/TA_WS/securities/announced/rss' \
  --htmlfile /private/tmp/treasann.html


