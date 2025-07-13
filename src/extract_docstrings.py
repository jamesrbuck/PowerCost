''' Extract docstring '''

import os
import ast
import markdown

def extract_docstrings_from_file(filepath):
    ''' extract_docstrings_from_file '''
    with open(filepath, "r", encoding="utf-8") as file:
        source = file.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Syntax error in {filepath}: {e}")
        return []

    docstrings = []

    # Module docstring
    module_doc = ast.get_docstring(tree)
    if module_doc:
        docstrings.append(("Module", filepath, module_doc))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            kind = type(node).__name__.replace("Def", "")
            doc = ast.get_docstring(node)
            if doc:
                docstrings.append((kind, name, doc))

    return docstrings

def extract_docstrings_from_directory(directory):
    ''' extract_docstrings_from_directory '''
    all_docstrings = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                docstrings = extract_docstrings_from_file(path)
                if docstrings:
                    all_docstrings.append((path, docstrings))

    return all_docstrings

def write_markdown(docstrings, output_file="DOCSTRINGS.md"):
    ''' write_markdown '''
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Project Documentation Extracted from Docstrings\n\n")
        for filepath, entries in docstrings:
            f.write(f"## File: `{filepath}`\n\n")
            for kind, name, doc in entries:
                if kind == "Module":
                    f.write(f"### 🧾 Module-level Docstring\n```\n{doc}\n```\n\n")
                else:
                    f.write(f"### {kind}: `{name}`\n```\n{doc}\n```\n\n")

if __name__ == "__main__":
    PROJECT_DIR = "powercost_project"
    BASEFILE = "powercost_project_docstrings"
    OUTMD = f"{BASEFILE}.md"
    OUTHTML = f"{BASEFILE}.html"
    my_docstrings = extract_docstrings_from_directory(PROJECT_DIR)
    write_markdown(my_docstrings, output_file=OUTMD)

    with open(OUTMD, 'r', encoding="utf-8") as md_file:
        text = md_file.read()

    html = markdown.markdown(text)
    with open(OUTHTML, 'w', encoding="utf-8") as html_file:
        html_file.write(html)
