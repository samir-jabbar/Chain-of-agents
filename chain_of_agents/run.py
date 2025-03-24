from rdflib import Graph

def load_ontology(file_path):
    """Load an ontology from a TTL file into an RDFLib Graph."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def extract_elements(graph):
    """Extract ontology elements (classes, properties, individuals) from a graph."""
    elements = set()
    for subj in graph.subjects():
        elements.add(str(subj))  # Convert RDF URI to string
    return elements

def compute_metrics(reference_ontology, generated_ontology):
    """Compute Conciseness, Completeness, and Correctness metrics."""
    common_elements = reference_ontology.intersection(generated_ontology)
    
    conciseness = len(common_elements) / len(generated_ontology) if generated_ontology else 0
    completeness = len(common_elements) / len(reference_ontology) if reference_ontology else 0
    
    if conciseness + completeness > 0:
        correctness = 2 * (conciseness * completeness) / (conciseness + completeness)
    else:
        correctness = 0
    
    return {
        "Conciseness": conciseness,
        "Completeness": completeness,
        "Correctness": correctness
    }

def main(reference_ttl, generated_ttl):
    """Main function to load ontologies, compute metrics, and print results."""
    reference_graph = load_ontology(reference_ttl)
    generated_graph = load_ontology(generated_ttl)
    
    reference_elements = extract_elements(reference_graph)
    generated_elements = extract_elements(generated_graph)
    
    metrics = compute_metrics(reference_elements, generated_elements)
    
    print("\nOntology Comparison Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
    
    return metrics

# Example usage (replace with your actual file paths)
reference_ttl_file = "pizza_onto_ground_truth.ttl"
generated_ttl_file = "ontology.ttl"

metrics_result = main(reference_ttl_file, generated_ttl_file)
