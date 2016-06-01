# Congressmembers who went to cool colleges

Which of our elected representatives earned their academic stripes -- or, even worked, or at least attended classes -- at America's best colleges (as ranked by U.S. News and World Report)? 

Its temporary home is here:
http://beta-congress-colleges-fun.s3-website-us-east-1.amazonaws.com/

This is an example of a (very simple) final project for the [Stanford Computational Journalism class](http://www.compjour.org).




## The data

This repo contains some code and data to mash up several data sources:

- Congressmember structured biographical information from https://github.com/unitedstates/congress-legislators
- Congressmember (unstructured) biographical information from http://bioguide.congress.gov/
  + See the code at: 
    + [scripts/bootstrap/fetch_bios.py](scripts/bootstrap/fetch_bios.py)
    + [scripts/bootstrap/extract_bio_text.py](scripts/bootstrap/extract_bio_text.py)
- [U.S. News and World Report Best Colleges of 2016](http://colleges.usnews.rankingsandreviews.com/best-colleges) - I actually just hand-copied the top 25 of both kinds of colleges and then added a regex pattern to match the variation of each school, as it might be listed in the bioguide entries, e.g. "University of California at Berkeley" and "University of California, Berkeley". It's not perfect, but most schools go by a fairly canonical and standardized name. You can see the lookup table at: [data/usnews/top_schools.csv](data/usnews/top_schools.csv)


## The wrangling

The script [scripts/bootstrap/filter_top_schools.py](scripts/bootstrap/filter_top_schools.py) contains a messy script that joins the unstructured bioguide text with proper school names.

The produced data files are in: [data/wrangled/](data/wrangled/)


## The app

This app is a fairly simple Flask app, not much different than the one described in the [First News App Tutorial](http://first-news-app.readthedocs.io/en/latest/).

It contains an example of __frozen deployment__ using the [Frozen Flask library](http://first-news-app.readthedocs.io/en/latest/#act-5-hello-internet). Just run [freeze.py](freeze.py) to generate a `build/` directory that can be uploaded to any static file server, including S3.


## Further work

I ended up classifying just the USN&amp;WR schools because there are just too many variations in how the BioGuide authors chose to describe life events. But there are plenty of other things to categorize, such as how many legislators were doctors/lawyers/small-town-mayors, or served in the military, or passed the bar, etc.


While there are 12,000+ total Congressmembers, there are enough incongruities in the biographical record (nevermind such things as colleges renaming themselves over the centuries) that it may be difficult to devise a purely machine-learning approach that isn't much more hacky and time-intensive than a focused crowd-sourced effort.

