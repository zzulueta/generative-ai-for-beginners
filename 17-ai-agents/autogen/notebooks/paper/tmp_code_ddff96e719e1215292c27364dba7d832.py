import json
from collections import Counter

# Data of categorized papers
papers = [
    {"title": "A novel approach to understanding the link between supermassive black holes and host galaxies", "category": "Not applicable"},
    {"title": "UTMath: Math Evaluation with Unit Test via Reasoning-to-Coding Thoughts", "category": "Fine Tuning"},
    {"title": "OpenThaiGPT 1.5: A Thai-Centric Open Source Large Language Model", "category": "Retrieval-Augmented Generation"},
    {"title": "DeepONet as a Multi-Operator Extrapolation Model: Distributed Pretraining with Physics-Informed Fine-Tuning", "category": "Fine Tuning"},
    {"title": "Contextualized Evaluations: Taking the Guesswork Out of Language Model Evaluations", "category": "Prompt Engineering"},
    {"title": "Score-based generative diffusion with 'active' correlated noise sources", "category": "Not applicable"},
    {"title": "Add-it: Training-Free Object Insertion in Images With Pretrained Diffusion Models", "category": "Fine Tuning"},
    {"title": "Watermark Anything with Localized Messages", "category": "Not applicable"},
    {"title": "Learning from Limited and Imperfect Data", "category": "Fine Tuning"},
    {"title": "Tooling or Not Tooling? The Impact of Tools on Language Agents for Chemistry Problem Solving", "category": "Agents"},
    {"title": "Modeling of non-planar slicer for improved surface quality in material extrusion 3D printing", "category": "Not applicable"},
    {"title": "TempCharBERT: Keystroke Dynamics for Continuous Access Control Based on Pre-trained Language Models", "category": "Fine Tuning"},
    {"title": "Grounding Video Models to Actions through Goal Conditioned Exploration", "category": "Agents"},
    {"title": "Gravitational production of massive vectors non-minimally coupled to gravity", "category": "Not applicable"},
    {"title": "Self-separated and self-connected models for mediator and outcome missingness in mediation analysis", "category": "Not applicable"},
    {"title": "wilson: A package for renormalization group running in the SMEFT with Sterile Neutrinos", "category": "Not applicable"},
    {"title": "TreeCoders: Trees of Transformers", "category": "Not applicable"},
    {"title": "Multifunctional spintronic transistors: Sub-60 mV/dec switching, non-local GMR, and NDR in spin gapless semiconductor and/or spin gapped metal FETs", "category": "Not applicable"},
    {"title": "Semantic Logical Relations for Timed Message-Passing Protocols (Extended Version)", "category": "Not applicable"},
    {"title": "Comparing Bottom-Up and Top-Down Steering Approaches on In-Context Learning Tasks", "category": "Prompt Engineering"}
]

# Filtering out "Not applicable" category
applicable_papers = [paper for paper in papers if paper["category"] != "Not applicable"]

# Counting the number of papers in each category
category_counts = Counter(paper["category"] for paper in applicable_papers)

# Sorting the categories based on the number of papers
sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

# Print the sorted categories and their counts
print(json.dumps(sorted_categories, indent=2))