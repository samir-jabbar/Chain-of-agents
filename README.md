# CoA-Text2OWL: Enhancing Ontology Learning with Chain-of-Agents Framework

This project implements the CoA (Chain-of-Agents) architecture to enhance the Text2OWL process, aiming to overcome the coherence, completeness, and scalability limitations of single-LLM ontology learning approaches. By distributing the task across multiple worker agents and a manager agent, CoA-Text2OWL enables more precise extraction of classes, object properties, and relationships from large and complex unstructured texts.

---

## Overview

**CoA-Text2OWL** introduces a Chain-of-Agents (CoA) paradigm for ontology learning (OL) from unstructured text. Instead of using a single LLM to directly generate an ontology, CoA-Text2OWL distributes the task across multiple worker agents and a manager agent, improving scalability, coherence, and completeness.

We evaluated CoA-Text2OWL against a traditional single-LLM Text2OWL method and demonstrated significant improvements, especially in extracting object properties.

## Architecture

- **Input Processing**: PDF parsing and text segmentation using PyMuPDF.
- **Chain-of-Agents Core**:
  - **Worker Agents**: Each processes a text chunk and generates partial OWL ontologies.
  - **Manager Agent**: Integrates outputs into a coherent final ontology.
- **Output Generation**: Final ontology serialized in OWL Turtle format.

All agents are powered by the Mistral models.

## Datasets

- **Pizza Ontology Texts**: Structured descriptions of pizzas used for baseline and comparative evaluation.
- **TRACES Project Data**: Real-world Geneva tramway and mobility policy documents.

## Repository Architecture

```bash
.
├── chain_of_agents/
│   ├── agents.py          # Definition of Worker and Manager agents
│   ├── main.py            # Main script to run the CoA workflow
│   ├── run.py             # Run configurations for experiments
│   ├── utils.py           # Helper functions
│   ├── __pycache__/       # Compiled python files
│   ├── bert_score_eval.ipynb      # Notebook for evaluating real-world ontologies
│   ├── pizza_results_analysis.ipynb # Notebook for Pizza dataset evaluation
│   ├── web_scraping.ipynb          # Notebook for scraping real-world data
│   ├── llm_owl_pizza_onto_mistral.ttl # Example output from LLM
│   ├── ontology.ttl       # Generated ontology output
│   └── TRACES PDFs        # Real-world input documents
├── pizza_description.pdf          # Pizza domain input text
├── pizza_description.txt          # Pizza domain input text (txt version)
├── pizza_onto_ground_truth.ttl     # Ground truth for Pizza Ontology
├── politiques_public_ontology.ttl  # Policy ontology output
├── tramway_ontology.ttl            # Tramway ontology output
├── run.sh                 # Shell script to execute the full workflow
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/coa-text2owl.git
cd coa-text2owl

# Install required packages
pip install -r requirements.txt
```

## Usage

To run the CoA-Text2OWL framework for ontology generation:
```bash
bash run.sh
```

To evaluate the generated ontologies against the Pizza ontology baseline:
- Open and run the notebook: `notebooks/pizza_results_analysis.ipynb`

For real-world use case (TRACES project):
- Scrape source data using: `notebooks/web_scraping.ipynb`
- Generate ontologies with `run.sh` script.
- Evaluate generated ontologies using: `notebooks/bert_score_eval.ipynb`

Make sure to adjust the input/output paths inside each notebook according to your project structure.
