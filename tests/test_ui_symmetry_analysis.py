import ast
import sys
from pathlib import Path

def check_symmetry(file_path):
    print(f"Checking {file_path}...", end=" ")
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print(f"Failed to parse: {e}")
        return False

    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for grid(), pack(), place(), or widget instantiation
            is_layout_call = False
            if isinstance(node.func, ast.Attribute) and node.func.attr in ("grid", "pack", "place"):
                is_layout_call = True
            elif isinstance(node.func, ast.Name) and node.func.id in ("Frame", "LabelFrame", "Button", "Label"): # Simplified check
                is_layout_call = True # catch kwarg padding in init
            elif isinstance(node.func, ast.Attribute) and node.func.attr in ("Frame", "LabelFrame", "Button", "Label"):
                 is_layout_call = True

            
            for keyword in node.keywords:
                if keyword.arg in ("padx", "pady", "padding"):
                    # Check if value is a Tuple
                    if isinstance(keyword.value, ast.Tuple):
                        # It's a tuple like (5, 10) or (0, 15)
                        # We consider this "asymmetric" because the user wants perfection/symmetry
                        # unless it's (10, 10) which is technically symmetric but redundant
                        
                        # Get detailed values if possible
                        values = []
                        for elt in keyword.value.elts:
                            if isinstance(elt, ast.Constant):
                                values.append(elt.value)
                            elif isinstance(elt, ast.Num): # Python < 3.8
                                values.append(elt.n)
                        
                        if len(values) == 2 and values[0] == values[1]:
                             # (10, 10) is fine
                             continue
                        if len(values) == 4 and values[0] == values[2] and values[1] == values[3]:
                             # (5, 10, 5, 10) is symmetric-ish but let's be strict
                             pass

                        issues.append(f"Line {node.lineno}: Asymmetric {keyword.arg}={values}")

    if issues:
        print("FAILED")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("PASSED")
        return True

files_to_check = [
    "modules/gui/multi_select_window.py",
    "modules/gui/ev_selection_window.py",
    "modules/gui/load_state_window.py",
    "modules/gui/create_profile_screen.py",
    "modules/gui/debug_edit_party.py",
]

all_passed = True
base_path = Path.cwd()

print("\n=== GUI Symmetry Audit ===\n")
for relative_path in files_to_check:
    full_path = base_path / relative_path
    if full_path.exists():
        if not check_symmetry(full_path):
            all_passed = False
    else:
        print(f"File not found: {relative_path}")

if all_passed:
    print("\n[SUCCESS] All checked files have symmetric padding.")
    sys.exit(0)
else:
    print("\n[FAILURE] Asymmetric padding detected.")
    sys.exit(1)
