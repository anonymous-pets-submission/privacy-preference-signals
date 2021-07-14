# Privacy Preference Signals: Past, Present and Future

📄 [Paper (petsymposium.org)](https://petsymposium.org/2021/files/papers/issue4/popets-2021-0069.pdf)  🎞️ [Presentation (YouTube)](https://youtu.be/-vsKzuVcq3o)

> Hils, M., Woods, D.W., and Böhme, R. Privacy Preference Signals: Past, Present and Future. *Proceedings on Privacy Enhancing Technologies*, 4 (2021). 

```bibtex
@article{hwb2021-pets,
 title = {Privacy Preference Signals: {P}ast, Present and Future},
 author = {Hils, Maximilian and Woods, Daniel W. and B{\"o}hme, Rainer},
 journal = {Proceedings on Privacy Enhancing Technologies},
 number = {4},
 year = {2021},
 url = {https://petsymposium.org/2021/files/papers/issue4/popets-2021-0069.pdf}
}
```

## Supplementary Material

This repository contains supplementary material for the PETS 2021 paper "Privacy Preference Signals: Past, Present and Future".

 - [`100k.feather`](https://github.com/anonymous-pets-submission/privacy-preference-signals/raw/main/100k.feather) contains the aggregated results from our snapshot crawl of the Tranco 100k.
It is stored as a [Feather](https://arrow.apache.org/docs/python/feather.html) file, which
can be easily accessed from both Python and R.
 - [`crawl`](./crawl) describes our crawling setup and includes all raw results.
 - [`tcf2-transition`](./tcf2-transition) details how we detect specific TCF versions for OneTrust and QuantCast and includes a copy of all historic GVL versions.
 - [`toplist-domains-to-urls`](./toplist-domains-to-urls) contains the code used to convert the Tranco toplist of domains
into a list of URLs that can be crawled.
 - [`popular-third-parties`](./popular-third-parties) contains a list of all popular third-party domains in the Tranco 100k.


### 100k.feather Column Descriptions
Column Descriptions:

 - **root:** The website's domain.
 - **rank:** The website's rank in our Tranco toplist.
 - **js_has_tcf1:** True if our JavaScript instrumentation detected TCFv1.x, False otherwise. 
 - **js_has_tcf2:** True if our JavaScript instrumentation detected TCFv2.x, False otherwise. 
 - **js_cmp_id:** The CMP identifier as self-reported by the website's CMP implementation.
 - **ngfetch_hosts:** The number of contacted second-level domains during the crawl, normalized using
   the public suffix list. This means that foo.example.com and bar.example.com will only count as one third party.
 - **ngfetch_google_tracking:** True if Google Analytics or Google Tag Manager were used on the website or in any subdocuments.
 - **ngfetch_google_ads:** True if Google Ads were embedded on the website or in any subdocuments, False otherwise.
 - **ngfetch_satellite_quantcast:** True if QuantCast's CMP domain was contacted.
 - **ngfetch_satellite_onetrust:** True if OneTrust's CMP domain was contacted.
 - **ngfetch_embeds_popular_third_party:** True if at least one [popular third party](./popular-third-parties) was contacted during the crawl, False otherwise.
 - **ngfetch_dom_text_includes_cookie:** True if the website's final DOM text included the word "cookie" (case-insensitive)
 - **ngfetch_https_only:** True if all (sub-)resources were loaded over HTTPS.
 - **ngfetch_sts_header:** True if at least one HTTP response from the root domain featured a `Strict-Transport-Security`
   header.
 - **ngfetch_cookie_httponly:** The fraction of all (including third-party) cookies that were set with the `HttpOnly` attribute.
 - **ngfetch_cookie_secure:** The fraction of all (including third-party) cookies that were set with the `Secure` attribute.
 - **netograph_tcf_onetrust:** The OneTrust TCF version as reported by our longitudinal measurements.
 - **netograph_tcf_quantcast:** The QuantCast TCF version as reported by our longitudinal measurements.
 - **netograph_cmp:** The current CMP as reported by our longitudinal measurements. Note that this is measured
   using very different methodology (see paper) and may lag behind the `js_` columns.
 - **category:** The website's category.
