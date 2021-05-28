# Tranco 100k Crawl

Due to GitHub's storage limits, we cannot include the full raw results of our snapshot crawl of the Tranco 100k here. We have included the crawl result for `example.com` here as a demonstration of what is captured with each crawl. See https://netograph.io/docs/ for details on the file formats.

## Crawl Details

Vantage Point: European University

Crawl Date: 2021-02-13 – 2021-02-19

User-Agent: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36`

## JavaScript Instrumentation

`browser-inject.js` contains the JavaScript code that is injected into each crawled website ten seconds after `DOMContentLoaded`. It looks available JS objects and attempts to interact with TCF implementations.
