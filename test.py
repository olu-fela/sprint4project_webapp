import streamlit as st
import nbformat
from nbconvert import ExecutePreprocessor
import os

# Function to run a Jupyter notebook
def run_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(notebook, {"metadata": {"path": os.path.dirname(notebook_path)}})

    # Extract and return outputs
    outputs = []
    for cell in notebook.cells:
        if cell.cell_type == "code":
            for output in cell.get("outputs", []):
                if output.output_type == "stream":
                    outputs.append(output.text)
                elif output.output_type == "execute_result":
                    outputs.append(output["data"]["text/plain"])
    return outputs

# Streamlit app
st.title("Run Jupyter Notebook in Streamlit")

# Specify the folder where notebooks are stored
notebook_folder = "./notebook"

# List all `.ipynb` files in the notebook folder
notebooks = [f for f in os.listdir(notebook_folder) if f.endswith(".ipynb")]

if not notebooks:
    st.warning("No notebooks found in the 'notebook' folder.")
else:
    # Select a notebook from the dropdown menu
    notebook_choice = st.selectbox("Select a notebook to run", notebooks)

    if st.button("Run Notebook"):
        notebook_path = os.path.join(notebook_folder, notebook_choice)
        st.write(f"Executing notebook: `{notebook_choice}`...")
        try:
            results = run_notebook(notebook_path)
            st.success("Notebook executed successfully!")
            st.write("### Notebook Outputs")
            for result in results:
                st.text(result)
        except Exception as e:
            st.error(f"An error occurred while executing the notebook: {e}")
