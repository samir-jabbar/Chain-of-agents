#!/bin/bash

# Exit on error
set -e
# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    /c/Users/Daren/AppData/Local/Programs/Python/Python312/python -m venv venv
fi

# Activate virtual environment
# Detect OS and activate virtual environment accordingly
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "TOGETHER_API_KEY=" > .env
    echo "Please add your Together API key to the .env file"
    exit 1
fi

# Run example
echo "Running Chain of Agents example..."
venv/Scripts/python - << EOF
from chain_of_agents import ChainOfAgents
from chain_of_agents.utils import read_pdf, split_into_chunks
from chain_of_agents.agents import WorkerAgent, ManagerAgent
import os
from dotenv import load_dotenv
import pathlib
import sys


# Initialize Chain of Agents
coa = ChainOfAgents(
    worker_model="mistral-large-2411",
    manager_model="mistral-large-2411",
    chunk_size=1024  # Reduced chunk size for better handling
)

# Read PDF file
pdf_path = "loi_réseau_transports_publics.pdf"  # Updated to your PDF file
if not os.path.exists(pdf_path):
    print(f"Error: PDF file not found at {pdf_path}")
    sys.exit(1)

input_text = read_pdf(pdf_path)
query = "Use the given text to construct an OWL ontology in the Turtle format"

# Process the text
print("\nProcessing document with Chain of Agents...\n")

chunks = split_into_chunks(input_text, coa.chunk_size, coa.worker_model)
worker_outputs = []
previous_cu = None

print("=" * 80)
print("WORKER RESPONSES")
print("=" * 80 + "\n")

for i, chunk in enumerate(chunks):
    print(f"\n{'='*30} Worker {i+1}/{len(chunks)} {'='*30}")
    worker = WorkerAgent(coa.worker_model, coa.worker_prompt)
    output = worker.process_chunk(chunk, query, previous_cu)
    worker_outputs.append(output)
    previous_cu = output
    print(f"\n{output}\n")

print("\n" + "=" * 80)
print("MANAGER SYNTHESIS")
print("=" * 80 + "\n")

manager = ManagerAgent(coa.manager_model, coa.manager_prompt)
final_output = manager.synthesize(worker_outputs, query)
print(final_output)

# Save the ontology to a Turtle file
ttl_filename = "ontology.ttl"
with open(ttl_filename, "w", encoding="utf-8") as ttl_file:
    ttl_file.write(final_output)
print(f"\nOntology saved to {ttl_filename}")

print("\n" + "=" * 80)
EOF

# Deactivate virtual environment
deactivate

echo "Done!" 