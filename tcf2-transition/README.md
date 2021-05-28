# Vendor Transitions

We include copies of all historic versions of the Global Vendor List in [`vendor-lists`](./vendor-lists).
The canonical sources for TCF 1.x have been taken down by the IAB.
Previous versions of the TCF 2.x vendor list can still be accessed at `https://vendorlist.consensu.org/v2/archives/vendor-list-v$VERSION.json`.

# Publisher Transitions

This file includes a short description on how we determine the TCF versions used by QuantCast and OneTrust.

All analyses are based on the historic captures recorded by [netograph.io](https://netograph.io). We analyze all captures that include 
requests to `cdn.cookielaw.org`, `cookie-cdn.cookiepro.com` and `quantcast.mgr.consensu.org`, which are domains contacted 
by the TCF implementations of OneTrust, OneTrust's CookiePro brand, and QuantCast respectively.
This yields about 302GB of logs for for OneTrust and 850GB of logs for QuantCast. We then extract all relevant URLs into 
a `(capture id, url)` table.

## QuantCast

We use the following SQL code to determine the TCF version in use:

```sql
DROP MATERIALIZED VIEW IF EXISTS urls_classifiers CASCADE;
CREATE MATERIALIZED VIEW urls_classifiers AS
SELECT id,
       MAX(substring(url from 'consensu\.org/choice/([^/]+)/'))                     AS v2_id,
       BOOL_OR(url ~ 'test\.quantcast\.mgr\.consensu\.org/GVL-v2/')                 AS v2_test,
       MAX(substring(url from 'consensu\.org/(v\d+)/cmp.js'))                       AS v1_pin,
       BOOL_OR(url ~ 'consensu\.org/(cmp\.js|qcu\.js|(v\d+/)?cmp-3pc-check\.html)') AS v1_latest
FROM urls
GROUP BY id;

CREATE MATERIALIZED VIEW qc_tcf_versions AS
WITH combined AS (
    SELECT id,
           CASE
               WHEN v2_id IS NOT NULL THEN 'v2_' || v2_id
               WHEN v2_test THEN 'v2_test'
               WHEN v1_pin IS NOT NULL THEN 'v1_' || v1_pin
               WHEN v1_latest THEN 'v1_latest'
               END AS version
    FROM urls_classifiers)
SELECT root,
       timestamp::date                        AS date,
       mode() WITHIN GROUP (ORDER BY version) AS version,
       MAX(id)                                AS sample_id
FROM combined
         NATURAL INNER JOIN capturelog
WHERE version IS NOT NULL
  AND root IS NOT NULL
GROUP BY root, date
ORDER BY root, date;
```

## OneTrust

We internally used a slightly more complex pipeline for OneTrust due to additional measurements we were trying to make,
but the results in the paper can be reproduced similar to above:

```sql
SELECT id,
       BOOL_OR(url ~ 'cdn\.cookielaw\.org/vendorlist/iab2Data\.json') AS v2_ot,
       BOOL_OR(url ~ 'cdn\.cookielaw\.org/vendorlist/iabData\.json') AS v1_ot,
       BOOL_OR(url ~ 'cookie-cdn\.cookiepro\.com/vendorlist/iab2Data\.json') AS v2_cookiepro,
       BOOL_OR(url ~ 'cookie-cdn\.cookiepro\.com/vendorlist/iabData\.json') AS v1_cookiepro
FROM urls
```
