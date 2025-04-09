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





