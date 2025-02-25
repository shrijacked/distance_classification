import os
import sys
import glob
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import nbformat

def test_notebook_resources():
    """Test if all resources referenced in Jupyter notebooks exist."""
    print("Testing notebook resources...")
    
    
    notebooks = glob.glob("**/*.ipynb", recursive=True)
    if not notebooks:
        print("No notebooks found.")
        return True
    
    print(f"Found {len(notebooks)} notebooks to check.")
    all_resources_exist = True
    
    for notebook_path in notebooks:
        print(f"\nChecking resources in {notebook_path}")
        try:
    
            notebook = nbformat.read(notebook_path, as_version=4)
            notebook_dir = os.path.dirname(notebook_path)
            
    
            for cell_num, cell in enumerate(notebook.cells):
                if cell.cell_type == 'code':
    
                    check_code_cell(cell, cell_num, notebook_dir, all_resources_exist)
                
                elif cell.cell_type == 'markdown':
    
                    check_markdown_cell(cell, cell_num, notebook_dir, all_resources_exist)
        
        except Exception as e:
            print(f"Error processing notebook {notebook_path}: {e}")
            all_resources_exist = False
    
    if all_resources_exist:
        print("\nAll resources exist!")
        return True
    else:
        print("\nSome resources are missing. See details above.")
        return False

def check_code_cell(cell, cell_num, notebook_dir, all_resources_exist):
    """Check code cells for file access operations."""
    code = cell.source
    
    
    file_operations = [
        "open(", "pd.read_csv(", "pd.read_excel(", 
        "plt.imread(", "Image(", "image.imread(", 
        "np.load(", "pd.read_"
    ]
    
    for line_num, line in enumerate(code.split('\n')):
        for op in file_operations:
            if op in line and ("'" in line or '"' in line):
    
                try:
    
                    quote_char = "'" if "'" in line else '"'
                    start = line.find(quote_char)
                    end = line.find(quote_char, start + 1)
                    if start > 0 and end > start:
                        filename = line[start+1:end]
    
                        if filename.startswith("http") or "$" in filename or "{" in filename:
                            continue
                        
    
                        file_path = os.path.join(notebook_dir, filename)
                        if not os.path.exists(file_path):
                            print(f"File not found (cell {cell_num}, line {line_num}): {filename}")
                            all_resources_exist = False
                        else:
                            print(f"Found file: {filename}")
                except:
                    continue

def check_markdown_cell(cell, cell_num, notebook_dir, all_resources_exist):
    """Check markdown cells for image references."""
    content = cell.source
    
    
    img_start = 0
    while True:
        img_start = content.find("![", img_start)
        if img_start == -1:
            break
        
    
        open_paren = content.find("(", img_start)
        if open_paren == -1:
            img_start += 2
            continue
        
        close_paren = content.find(")", open_paren)
        if close_paren == -1:
            img_start = open_paren + 1
            continue
        
    
        img_path = content[open_paren+1:close_paren]
        
    
        if img_path.startswith("http"):
            img_start = close_paren + 1
            continue
        
    
        file_path = os.path.join(notebook_dir, img_path)
        if not os.path.exists(file_path):
            print(f"Image not found (markdown cell {cell_num}): {img_path}")
            all_resources_exist = False
        else:
            print(f"  ✓ Found image: {img_path}")
        
        img_start = close_paren + 1

if __name__ == "__main__":
    success = test_notebook_resources()
    if not success:
        sys.exit(1)  
    sys.exit(0)  