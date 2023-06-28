import os
import streamlit as st
import cadquery as cq

ALLOWED_EXTENSIONS = {'step', 'stp', 'iges'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_bounding_box_dimensions(shape):
    bb = shape.val().BoundingBox()
    dimensions = (bb.xmax - bb.xmin, bb.ymax - bb.ymin, bb.zmax - bb.zmin)
    return dimensions

def display_measurements(dimensions):
    st.write(f"Length (X): {dimensions[0]}")
    st.write(f"Width  (Y): {dimensions[1]}")
    st.write(f"Height (Z): {dimensions[2]}")

def display_detailed_measurements(shape):
    faces = shape.faces().vals()
    edges = shape.edges().vals()

    st.write("### Face Areas")
    for i, face in enumerate(faces, start=1):
        area = face.Area()
        st.write(f"Face {i}: {area}")

    st.write("### Edge Lengths")
    for i, edge in enumerate(edges, start=1):
        length = edge.Length()
        st.write(f"Edge {i}: {length}")

def load_cad_model(file_path, ext):
    return (
        cq.importers.importStep(file_path)
        if ext in ["step", "stp"]
        else cq.importers.importShape(file_path, file_ext)
    )

def main():
    st.title("Upload CAD File")
    uploaded_file = st.file_uploader(
        "Choose a CAD file to upload",
        type=ALLOWED_EXTENSIONS,
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        ext = uploaded_file.name.split(".", 1)[1].lower()
        filename = f"temp.{ext}"
        with open(filename, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        model = load_cad_model(filename, ext)
        dimensions = get_bounding_box_dimensions(model)

        display_measurements(dimensions)
        display_detailed_measurements(model)

if __name__ == "__main__":
    main()