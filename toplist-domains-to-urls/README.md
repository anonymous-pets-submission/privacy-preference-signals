This directory contains the code used to convert domains into URLs that can be crawled.

 - `check-availability.py` attempts to connect to all domains in a `rank,domain` 
   Tranco toplist csv passed via stdin, 
   both with and without HTTPS and with and without `www.` prefix. 
   Results are stored in a SQLite database. 
   Run repeatedly to accomodate temporary service disruptions.
 - `export-urls.py` accepts the same `rank,domain` toplist via stdin and 
   outputs a `rank,url` csv file.
