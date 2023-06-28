import os
import streamlit as st
import cadquery as cq

#Testing

ALLOWED_EXTENSIONS = {'step', 'stp', 'iges'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_bounding_box_dimensions(shape):
    print(type(shape))  # Add this line to check the type of the shape variable
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

def main():
    st.title("Upload CAD File")
    uploaded_file = st.file_uploader(
        "Choose a CAD file to upload",
        type=ALLOWED_EXTENSIONS,
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        file_ext = uploaded_file.name.rsplit(".", 1)[1].lower()
        file_content = uploaded_file.read()
        input_path = f'temporary.{file_ext}'
        with open(input_path, "wb") as f:
            f.write(file_content)

        loaded_model = (
            cq.importers.importStep(input_path)
            if file_ext in ["step", "stp"]
            else cq.importers.importers.importShape(input_path, file_ext)
        )
        shape = loaded_model
        dimensions = get_bounding_box_dimensions(shape)

        display_measurements(dimensions)
        display_detailed_measurements(shape)

if __name__ == "__main__":
    main()
