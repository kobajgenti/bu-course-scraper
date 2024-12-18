import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from pathlib import Path

def get_total_pages(url, headers):
    """Determine the total number of pages for a college."""
    try:
        response = requests.get(url + "1/", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the pagination div
        pagination = soup.find('div', class_='pagination')
        if pagination:
            # Get the last span element within pagination
            last_span = pagination.find_all('span')[-1]
            if last_span:
                # Find the link within the last span and extract the number
                last_page_link = last_span.find('a')
                if last_page_link:
                    # Extract the number from the URL
                    last_page = last_page_link.text.strip()
                    return int(last_page)
        
        print(f"Warning: Could not find pagination for {url}, checking if single page exists")
        # Check if there's at least one page of content
        course_feed = soup.find('ul', class_='course-feed')
        return 1 if course_feed else 0
        
    except Exception as e:
        print(f"Error getting total pages: {str(e)}")
        return 0

def scrape_bu_college_courses(college_code):
    """Scrape courses for a specific college."""
    all_courses = []
    
    # Base URL for the college
    base_url = f"https://www.bu.edu/academics/{college_code.lower()}/courses/"
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Get total number of pages
    total_pages = get_total_pages(base_url, headers)
    print(f"Found {total_pages} pages for {college_code.upper()}")
    
    # Iterate through all pages
    for page in range(1, total_pages + 1):
        try:
            # Construct page URL
            url = f"{base_url}{page}/"
            
            # Get page content
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find course-feed
            course_feed = soup.find('ul', class_='course-feed')
            
            if course_feed:
                # Find all course items
                courses = course_feed.find_all('li')
                
                for course in courses:
                    # Extract course title
                    title_element = course.find('strong')
                    if title_element:
                        title = title_element.text.strip()
                    else:
                        continue
                    
                    # Extract description (text after <br> tag)
                    description = ''
                    br_tag = course.find('br')
                    if br_tag:
                        description = br_tag.next_sibling.strip()
                    
                    # Add to our list
                    all_courses.append({
                        'college': college_code.upper(),
                        'title': title,
                        'description': description
                    })
            
            # Add a small delay to be nice to the server
            time.sleep(1)
            
            # Print progress
            print(f"{college_code.upper()}: Processed page {page}/{total_pages}")
            
        except Exception as e:
            print(f"Error on {college_code.upper()} page {page}: {str(e)}")
            continue
    
    return all_courses

def main():
    # List of BU colleges
    bu_abbreviations = [
        "bua", "cas", "cfa", "cgs", "com", "eng", "egs", "eop", "gms", "grs",
        "hub", "khc", "law", "med", "met", "otp", "pdp", "qst", "sar", "sed",
        "sdm", "sha", "sph", "ssw", "sth", "sum", "uni", "xrg"
    ]
    
    # Create output directory if it doesn't exist
    output_dir = Path('bu_courses')
    output_dir.mkdir(exist_ok=True)
    
    # Process each college
    for college in bu_abbreviations:
        print(f"\nStarting to scrape {college.upper()} courses...")
        
        # Scrape courses for this college
        courses = scrape_bu_college_courses(college)
        
        if courses:
            # Convert to DataFrame
            df = pd.DataFrame(courses)
            
            # Save to CSV
            output_file = output_dir / f'{college}_courses.csv'
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Completed {college.upper()}! Found {len(df)} courses.")
            print(f"Data saved to '{output_file}'")
        else:
            print(f"No courses found for {college.upper()}")

if __name__ == "__main__":
    print("Starting to scrape all BU colleges...")
    main()
    print("\nScraping complete!")