from ladybug_geometry.geometry3d import Point3D, Face3D, Polyface3D, Vector3D
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
from honeybee.model import Model,Room
import json
import web as web
import tempfile
from pathlib import Path
from honeybee.boundarycondition import boundary_conditions
import pollination_streamlit_viewer as ps
import pandas as pd
from utils import get_lighting_gains,get_occupancy_gains,get_elec_equip_gains,get_infiltration_gains
from honeybee_energy.lib.programtypes import STANDARDS_REGISTRY
from honeybee_energy.lib.programtypes import PROGRAM_TYPES
from honeybee_energy.lib.programtypes import program_type_by_identifier
from honeybee_energy.lib.programtypes import BUILDING_TYPES
from honeybee.search import filter_array_by_keywords
import random
import uuid

#def clear_temp_folder():
    #st.session_state.temp_folder = Path(tempfile.mkdtemp())

def initialize():
    if "footprint" not in st.session_state: 
        st.session_state.footprint = None
    if "no_of_floors" not in st.session_state: 
        st.session_state.no_of_floors = None
    if "floor_height" not in st.session_state: 
        st.session_state.floor_height = None      
    if "wwr" not in st.session_state: 
        st.session_state.wwr = None
    if "building_geometry" not in st.session_state: 
        st.session_state.building_geometry = None       
    if "hb_model" not in st.session_state: 
        st.session_state.hb_model = None
    if "temp_folder" not in st.session_state: 
        st.session_state.temp_folder = Path(tempfile.mkdtemp()) #not going to generate a local file, just creates a temporary file in memory
    if "hb_json_path" not in st.session_state: 
        st.session_state.hb_json_path = None
    if "visualize" not in st.session_state: 
        st.session_state.visualize = None
    if "vintage" not in st.session_state:
        st.session_state.vintage = None
    if "building_type" not in st.session_state:
        st.session_state.building_type = None

def display_model_geometry():
    #requirements to display a model:
        #1. Have a temporary folder
        #2. 
        
    st.session_state.hb_json_path = st.session_state.temp_folder.joinpath(f"{st.session_state.hb_model.identifier}.hbjson")
    st.session_state.hb_json_path.write_text(json.dumps(st.session_state.hb_model.to_dict()))
    web.show_model(st.session_state.hb_json_path)

def upload_hbjson_file():
    st.title("Honeybee JSON 3D Model Viewer")
    
    # Upload Honeybee JSON file
    uploaded_file = st.file_uploader("Upload a Honeybee JSON (*.hbjson) file", type=["json"])
    
    if uploaded_file is not None:
        # Read and parse the JSON file
        try:
            hbjson_data = json.load(uploaded_file)
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid *.json file.")
            return
        
        # Check if the JSON file contains a Honeybee model
        if "type" in hbjson_data and hbjson_data["type"] == "Model":
            st.success("Honeybee JSON file successfully loaded.")
            
            # Create a Honeybee model object from the deserialized data
            st.session_state.hb_model = Model.from_dict(hbjson_data)
            
            # Visualize the 3D model using Polination Streamlit Viewer
            display_model_geometry()
        else:
            st.error("The uploaded JSON file does not contain a valid Honeybee model.")


def iterate_rooms_and_display_properties():
    # Check if the provided object is a Honeybee model
    if not isinstance(st.session_state.hb_model, Model):
        st.error("Invalid input. Please provide a valid Honeybee model object.")
        return

    # Create an empty list to store room properties
    room_data = []

    # Iterate over rooms in the model
    # TODO - Allow user to modify specific program properties, i.e. lighting power, people sensible gain, etc..
    # TODO - Allow user to assign HVAC system per room. HVAC systems from Honeybee HVAC models
    # New APP from here...
    # TODO - Upload weather file OR download from ladybug weather file database
    # TODO - Allow user to run sim and load results

         
    st.session_state.vintage = st.selectbox('Construction Period:',list(STANDARDS_REGISTRY),6)
    st.session_state.building_type = st.selectbox('Building Type:',list(BUILDING_TYPES),6)
    room_prog = filter_array_by_keywords(PROGRAM_TYPES, [st.session_state.vintage,st.session_state.building_type], False)
    
    for room in st.session_state.hb_model.rooms:
        if not room.user_data:
            room.user_data = {'room_prog':random.choice(room_prog)}
            # if not room.properties.energy.program_type:
            # room.properties.energy.program_type = program_type_by_identifier(room.user_data['room_prog'])

    # Display the room properties in Streamlit
    st.write("Room Properties:")
    #room_df_edited = st.data_editor(room_df)

    # Display each room's properties using expanders
    for room in st.session_state.hb_model.rooms:
        with st.expander(f"Room identifier: {room.identifier}"):
            # Display each property
            st.write("Floor area")
            st.code(room.floor_area)
            room.display_name = st.text_input("Display name", room.display_name)
            # Use room.identifier to generate a consistent key for the selectbox
            selectbox_key = f"room_prog_{room.identifier}"
            current_prog_index = room_prog.index(room.properties.energy.program_type.identifier)
            new_room_prog = st.selectbox(label="Room Program",
                                     options=room_prog,
                                     index=current_prog_index,
                                     key=selectbox_key)
            room.properties.energy.program_type = program_type_by_identifier(new_room_prog)
            st.write("Lighting gains")
            st.json(room.properties.energy.program_type.lighting.to_dict() if room.properties.energy.program_type.lighting else {},expanded=False)
            st.write("People gains")
            st.json(room.properties.energy.program_type.people.to_dict() if room.properties.energy.program_type.people else {}, expanded=False)
            st.write("Elec equipment gains")
            st.json(room.properties.energy.program_type.electric_equipment.to_dict() if room.properties.energy.program_type.electric_equipment else {}, expanded=False)
            st.write("Gas equipment gains")
            st.json(room.properties.energy.program_type.gas_equipment.to_dict() if room.properties.energy.program_type.gas_equipment else {}, expanded=False)
            st.write("Service Hot Water")
            st.json(room.properties.energy.program_type.service_hot_water.to_dict() if room.properties.energy.program_type.service_hot_water else {}, expanded=False)
            st.write("Infiltration")
            st.json(room.properties.energy.program_type.infiltration.to_dict() if room.properties.energy.program_type.infiltration else {}, expanded=False)
            st.write("Ventilation")
            st.json(room.properties.energy.program_type.ventilation.to_dict() if room.properties.energy.program_type.ventilation else {}, expanded=False)
            st.write("Set point")
            st.json(room.properties.energy.program_type.setpoint.to_dict() if room.properties.energy.program_type.setpoint else {}, expanded=False)
