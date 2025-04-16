from googlesearch import search
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=5):
    return list(search(query, num_results=num_results, lang="en"))

def scrape_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return '\n'.join(paragraphs[:5])  
    except Exception as e:
        return f"Failed to scrape {url}: {str(e)}"

def seo_agent_no_api(prompt):
    print(f"Searching: {prompt}")
    urls = google_search(prompt)
    print("\nTop Links Found:\n", "\n".join(urls))
    
    content = ""
    for url in urls:
        print(f"\nScraping: {url}")
        scraped = scrape_page(url)
        content += scraped + "\n---\n"
    
    print("\n--- Combined Snippets ---\n")
    print(content[:2000]) 
    return content


if __name__ == "__main__":
    user_input = input("Enter your SEO prompt: ")
    seo_agent_no_api(user_input)
