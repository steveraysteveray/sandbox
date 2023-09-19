import argparse
import rdflib

def find_ontology_base(file_path):
    g = rdflib.Graph()
    g.parse(file_path, format='turtle')
    
    for s in g.subjects(predicate=rdflib.RDF.type, object=rdflib.OWL.Ontology):
        return str(s)
    return None

def add_base_if_missing(file_path):
    base_uri = find_ontology_base(file_path)
    if base_uri is None:
        print("No owl:Ontology found in the RDF file!")
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Insert the @base declaration before line #4
    if "@base" not in lines[3]:  # Checking to ensure it's not already added
        lines.insert(3, f"@base <{base_uri}> .\n")

    with open(file_path, 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add @base to an RDF Turtle file if it is missing.')
    parser.add_argument('file_path', help='Path to the RDF Turtle file.')

    args = parser.parse_args()

    add_base_if_missing(args.file_path)