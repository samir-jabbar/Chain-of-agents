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
├── data/
│   ├── inputs/              # Place your input files here (PDFs, text files)
│   └── outputs/             # Generated outputs (ontologies, results)
├── chain_of_agents/
│   ├── agents.py          # Definition of Worker and Manager agents
│   ├── main.py            # Main script to run the CoA workflow
│   ├── run.py             # Run configurations for experiments
│   ├── utils.py           # Helper functions
│   ├── data/
│   │   ├── inputs/        # Input files for this module
│   │   └── outputs/       # Output files from this module
│   ├── bert_score_eval.ipynb      # Notebook for evaluating real-world ontologies
│   ├── pizza_results_analysis.ipynb # Notebook for Pizza dataset evaluation
│   └── web_scraping.ipynb          # Notebook for scraping real-world data
├── run.sh                 # Shell script to execute the full workflow
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation (this file)
└── .env.example           # Environment variables template
```

## Installation

### Prerequisites
- Python 3.8 or higher
- A Mistral AI API key (get it from https://console.mistral.ai/)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/your-org/coa-text2owl.git
cd coa-text2owl

# Install required packages
pip install -r requirements.txt

### Environment Configuration

The project requires a `.env` file with your API credentials.

Create `.env` and add your API keys:
   ```
   MISTRAL_API_KEY=your_actual_api_key_here
   ```

## Usage

### Data Organization

All input and output files are organized in the `data/` directory:
- **`data/inputs/`**: Place your PDF files, text files, and ground truth ontologies here
- **`data/outputs/`**: Generated ontologies and results will be saved here

### Running the Pipeline

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

