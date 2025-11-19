from flask import Flask, request, jsonify, Response, stream_with_context
from chain_of_agents import ChainOfAgents
from chain_of_agents.utils import read_pdf
from dotenv import load_dotenv
import json
import os
import logging
from pathlib import Path

# Load environment variables
load_dotenv()

# Define data directories
DATA_ROOT = Path(__file__).parent / "data"
INPUTS_DIR = DATA_ROOT / "inputs"
OUTPUTS_DIR = DATA_ROOT / "outputs"

# Ensure directories exist
INPUTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
coa = ChainOfAgents(
    worker_model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    manager_model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    chunk_size=2000
)

logger = logging.getLogger(__name__)

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    input_text = data.get('text')
    query = data.get('query')
    
    try:
        result = coa.process(input_text, query)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process-stream', methods=['POST'])
def process_stream():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    pdf_file = request.files['pdf']
    query = request.form.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Save PDF temporarily to inputs directory
    temp_path = INPUTS_DIR / 'temp.pdf'
    pdf_file.save(str(temp_path))
    
    try:
        # Extract text from PDF
        input_text = read_pdf(str(temp_path))
        
        def generate():
            try:
                for message in coa.process_stream(input_text, query):
                    formatted_message = f"data: {json.dumps(message)}\n\n"
                    logger.info(f"Sending SSE message: {formatted_message}")  # Debug log
                    yield formatted_message
            except Exception as e:
                error_message = f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
                logger.error(f"Error message: {error_message}")  # Debug log
                yield error_message
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    
    finally:
        # Clean up temporary file
        if temp_path.exists():
            temp_path.unlink()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 