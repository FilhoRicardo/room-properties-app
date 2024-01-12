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




def clear_temp_folder():
    st.session_state.temp_folder = Path(tempfile.mkdtemp())

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

def get_all_room_properties(room):
    """Recursively collect all room properties."""
    properties = {}
    for key, value in room.__dict__.items():
        if isinstance(value, (int, float, str, bool, list)):
            properties[key] = value
        elif isinstance(value, dict):
            properties[key] = {k: v for k, v in value.items() if isinstance(v, (int, float, str, bool, list))}
        elif isinstance(value, Room):
            properties[key] = get_all_room_properties(value)
    return properties

def iterate_rooms_and_display_properties():
    # Check if the provided object is a Honeybee model
    if not isinstance(st.session_state.hb_model, Model):
        st.error("Invalid input. Please provide a valid Honeybee model object.")
        return

    # Create an empty list to store room properties
    room_data = []

    # Iterate over rooms in the model

    # TODO - Create dropdown per room to allow program type selection
    # TODO - allow user to make changes and make sure they are saved back in the model via the application
    # TODO - allow user to download model 
    
    st.session_state.vintage = st.selectbox('Construction Period:',list(STANDARDS_REGISTRY),6)
    st.session_state.building_type = st.selectbox('Building Type:',list(BUILDING_TYPES),6)
    room_prog = filter_array_by_keywords(PROGRAM_TYPES, [st.session_state.vintage,st.session_state.building_type], False)
    
    for room in st.session_state.hb_model.rooms:
        '''if not room.properties.energy.people:
            room.properties.energy.people = get_occupancy_gains(room)
        if not room.properties.energy.lighting:
            room.properties.energy.lighting = get_lighting_gains(room)
        if not room.properties.energy.electric_equipment:
            room.properties.energy.electric_equipment = get_elec_equip_gains(room)
        if not room.properties.energy.infiltration:
            room.properties.energy.infiltration = get_infiltration_gains(room)'''
        if not room.user_data:
            room.user_data = {'room_prog':random.choice(room_prog)}
        # if not room.properties.energy.program_type:
        room.properties.energy.program_type = program_type_by_identifier(room.user_data['room_prog'])


        
        room_properties = {
            "Display name": room.display_name,
            "Room identifier": room.identifier,
            "Room Program": room.user_data['room_prog'],
            "Floor area": room.floor_area,
            "Lighting gains": room.properties.energy.program_type.lighting.to_dict() if room.properties.energy.program_type.lighting else None,
            "People gains": room.properties.energy.program_type.people.to_dict() if room.properties.energy.program_type.people else None,
            "Elec equipment gains": room.properties.energy.program_type.electric_equipment.to_dict() if room.properties.energy.program_type.electric_equipment else None,
            "Gas equipment gains": room.properties.energy.program_type.gas_equipment.to_dict() if room.properties.energy.program_type.gas_equipment else None,
            "Service Hot Water": room.properties.energy.program_type.service_hot_water.to_dict() if room.properties.energy.program_type.service_hot_water else None,
            "Infiltration": room.properties.energy.program_type.infiltration.to_dict() if room.properties.energy.program_type.infiltration else None,
            "Ventilation": room.properties.energy.program_type.ventilation.to_dict() if room.properties.energy.program_type.ventilation else None,
            "Set point": room.properties.energy.program_type.setpoint.to_dict() if room.properties.energy.program_type.setpoint else None
        }
        room_data.append(room_properties)

    # Create a DataFrame from the collected room data
    room_df = pd.DataFrame(room_data)

    # Display the room properties in Streamlit
    st.write("Room Properties:")
    #room_df_edited = st.data_editor(room_df)

    # Display each room's properties using expanders
    for index, room in room_df.iterrows():
        with st.expander(f"Room: {room['Display name']}"):
            # Display each property
            for key, value in room.items():
                st.write(f"{key}:")
                if key == "Room Program":
                    st.selectbox(label=key,options=room_prog,key=str(uuid.uuid4()))
                elif isinstance(value, dict):
                    # Use st.json for complex dictionary types like 'schedule'
                    st.json(value)
                else:
                    st.write(value)

# Example usage:
# Iterate over rooms and display their properties
# You can replace 'hb_model' with your Honeybee model object
# iterate_rooms_and_display_properties(hb_model)



def geometry_parameters(container):
    width_ = container.slider("Building Width [m]",min_value=0,max_value=50,value=10,help="This is the width of the building in meters")
    lenght_ = container.slider("Building Lenght [m]",min_value=0,max_value=50,value=10,help="This is the lenght of the building in meters")        
    no_of_floors_ = container.slider("Number of floors",min_value=0,max_value=6,value=1,step=1,help="This is the lenght of the building in meters")
    floor_height_ = container.slider("Building Floor height [m]",min_value=2,max_value=10,value=3,help="This is the height of the building floor in meters")       
    wwr_ =  container.slider("Window to wall ratio",min_value=0.0,max_value=0.99,value=0.4,help="This is the window to wall ratio for all the rooms")
   

    lower_left = Point3D(0, 0, 0)
    lower_right = Point3D(width_, 0, 0)
    upper_right = Point3D(width_, lenght_, 0)
    upper_left = Point3D(0, lenght_, 0)

    st.session_state.footprint = [lower_left, lower_right, upper_right, upper_left]
    st.session_state.no_of_floors = no_of_floors_
    st.session_state.floor_height = floor_height_
    st.session_state.wwr = wwr_

def generate_building1(footprint, floor_height, num_floors):
    all_floors = []

    for i in range(num_floors):
        faces = []
        base_height = i * floor_height
        upper_height = (i + 1) * floor_height

        # Bottom face for the current floor (also serves as ceiling for the floor below)
        faces.append(Face3D([pt.move(Vector3D(0, 0, base_height)) for pt in footprint]))

        # Side faces for the current floor
        for j in range(len(footprint)):
            start_point = footprint[j]
            end_point = footprint[(j + 1) % len(footprint)]

            lower_left = Point3D(start_point.x, start_point.y, base_height)
            lower_right = Point3D(end_point.x, end_point.y, base_height)
            upper_right = Point3D(end_point.x, end_point.y, upper_height)
            upper_left = Point3D(start_point.x, start_point.y, upper_height)

            face = Face3D([lower_left, lower_right, upper_right, upper_left])
            faces.append(face)

        # Top face for the current floor
        if i == num_floors - 1:
            faces.append(Face3D([pt.move(Vector3D(0, 0, upper_height)) for pt in footprint]))

        floor_geometry = Polyface3D.from_faces(faces, 0.01)
        all_floors.append(floor_geometry)

    st.session_state.building_geometries = all_floors  # Store the list of Polyface3D geometries for each floor


def generate_building(footprint, floor_height, num_floors):
    all_floors = []

    for i in range(num_floors):
        faces = []
        base_height = i * floor_height
        upper_height = (i + 1) * floor_height

        # Bottom face for every floor (also serves as ceiling for the floor below)
        faces.append(Face3D([pt.move(Vector3D(0, 0, base_height)) for pt in footprint]))

        # Side faces for the current floor
        for j in range(len(footprint)):
            start_point = footprint[j]
            end_point = footprint[(j + 1) % len(footprint)]

            lower_left = Point3D(start_point.x, start_point.y, base_height)
            lower_right = Point3D(end_point.x, end_point.y, base_height)
            upper_right = Point3D(end_point.x, end_point.y, upper_height)
            upper_left = Point3D(start_point.x, start_point.y, upper_height)

            face = Face3D([lower_left, lower_right, upper_right, upper_left])
            faces.append(face)

        # Top face for every floor including the very bottom one
        faces.append(Face3D([pt.move(Vector3D(0, 0, upper_height)) for pt in footprint]))

        floor_geometry = Polyface3D.from_faces(faces, 0.01)
        all_floors.append(floor_geometry)

    st.session_state.building_geometries = all_floors  # Store the list of Polyface3D geometries for each floor

def generate_honeybee_model():
    """Type of building: Polyface3D"""
    """This function will convert the building into a Honeybee JSON"""

    st.session_state.hb_model = Model("shoeBox")  # instantiate a model
    rooms = []  # to store all rooms for adjacency check

    for i, floor_geometry in enumerate(st.session_state.building_geometries):
        room = Room.from_polyface3d(f"room_{i}", floor_geometry)  # creating a room
        room.wall_apertures_by_ratio(st.session_state.wwr)  # add a window

        rooms.append(room)  # append room to the list
        st.session_state.hb_model.add_room(room)  # adding a room to the model

    # Solve adjacency between rooms
    Room.solve_adjacency(st.session_state.hb_model.rooms, 0.01)



def get_model_info():
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric(label=f"Total Volume",value=st.session_state.hb_model.volume)
    with col2:
        st.metric(label="Total area",value=st.session_state.hb_model.floor_area)
    with col3:
        st.metric(label="Total glazing area",value=round(st.session_state.hb_model.exterior_aperture_area,1))

   
def parameters_changed():
    """Check if the building parameters have changed from previous version.
        parameter name: 
    """
    keys = ['footprint', 'no_of_floors', 'floor_height', 'wwr']
    for key in keys:
        if key + "_old" not in st.session_state:
            st.session_state[key + "_old"] = st.session_state[key]
        elif st.session_state[key + "_old"] != st.session_state[key]:
            st.session_state[key + "_old"] = st.session_state[key]
            return True
    return False
