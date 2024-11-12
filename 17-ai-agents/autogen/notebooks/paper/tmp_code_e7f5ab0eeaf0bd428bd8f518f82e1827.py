import arxiv
import json

# Function to search for the latest papers on Large Language Models
def fetch_latest_papers(query="Large Language Models", max_results=20):
    # Search for papers
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    # Extract relevant data
    papers = []
    for result in search.results():
        paper_info = {
            "title": result.title,
            "abstract": result.summary
        }
        papers.append(paper_info)
    
    return papers


# Fetch 20 latest papers on Large Language Models
latest_papers = fetch_latest_papers()

# Print the results
print(json.dumps(latest_papers, indent=2))