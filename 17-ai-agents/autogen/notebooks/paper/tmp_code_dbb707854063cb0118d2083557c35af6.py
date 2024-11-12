import requests
import xml.etree.ElementTree as ET

def fetch_latest_papers(query="Large Language Models", max_results=20):
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:{query}',
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from arXiv API: {response.status_code}")

    root = ET.fromstring(response.content)
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        papers.append({'title': title, 'summary': summary})

    return papers

# Fetch the latest 20 papers on Large Language Models
papers = fetch_latest_papers()

# Print the abstracts for the Scientist to categorize
for i, paper in enumerate(papers):
    print(f"\nPaper {i+1}: {paper['title']}")
    print(f"Abstract: {paper['summary']}")