from googlesearch import search
import requests
from bs4 import BeautifulSoup
from transformers import pipeline


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def google_search(query, num_results=5):
    results = []
    for url in search(query, num_results=num_results, lang="en"):
        if url.startswith("http"):
            results.append(url)
    return results

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

def summarize_text(text, max_tokens=130):
    try:
        if len(text.strip()) == 0:
            return "No content to summarize."
        summary = summarizer(text, max_length=max_tokens, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Summarization error: {str(e)}"

def seo_agent_with_summary(prompt):
    print(f"Searching: {prompt}")
    urls = google_search(prompt)
    print("\nTop Links Found:\n", "\n".join(urls))
    
    combined_content = ""
    for url in urls:
        print(f"\nScraping: {url}")
        content = scrape_page(url)
        combined_content += content + "\n---\n"
    
    print("\n--- Summarized Answer ---\n")
    summarized_answer = summarize_text(combined_content[:3000])  
    print(summarized_answer)
    return summarized_answer


if __name__ == "__main__":
    user_input = input("Enter your SEO prompt: ")
    seo_agent_with_summary(user_input)
