# BU Course Data Scraper

A simple web scraper I built for a part of a class project to collect all course data from Boston University. Turns out BU has over **11 008** courses across all colleges which is pretty wild!

I couldn't find this data publicly available anywhere, so hopefully this helps.


## Data Files

The repository contains course data for Fall 2024:
- Individual CSV files for each college/school under `/bu_courses/`
- Combined dataset: `bu_all_courses.csv`
- Firebase-ready structure: `bu_courses_firebase.json`

## Code
- `main.py`: Python script to scrape fresh course data from BU's website
- `format.ipynb`: Jupyter notebook for combining CSVs and formatting data for Firebase

## Source
Data scraped from: https://www.bu.edu/academics/

Feel free to use this data for your own projects. Just keep in mind it's from Fall 2024 and courses/descriptions might change.

Enjoy! 🎓

