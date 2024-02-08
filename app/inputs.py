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
import copy


# Iterate over rooms in the model
    # TODO - Allow user to assign HVAC system per room. HVAC systems from Honeybee HVAC models
    # New APP from here...
    # TODO - Upload weather file OR download from ladybug weather file database
    # TODO - Allow user to run sim
    # TODO - Allow user to run parametric sims - changing design properties (WW ratio, u-values, shading %...)
    # New App from here...
    # TODO - Visualization tool compliant with ASHRAE 209
   
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

def update_properties_dict(room, properties_dict, property_name, parent_key=''):
    updated_dict = copy.deepcopy(properties_dict)  # Use deepcopy to handle nested dicts correctly
    for key, value in properties_dict.items():
        unique_key = f"{parent_key}_{key}" if parent_key else key
        input_key = f"{room.identifier}_{property_name}_{unique_key}"

        if isinstance(value, dict):
            #updated_dict[key] = update_properties_dict(room, value, property_name, unique_key)
            st.write(key)
            st.json(value,expanded=False)
        elif isinstance(value, str):
            continue
        else:
            # Handling different data types
            new_value = st.text_input(f"{unique_key}:", value=str(value), key=input_key)
            if isinstance(value, float):
                try:
                    updated_dict[key] = float(new_value)
                except ValueError:
                    st.error(f"Invalid input for {unique_key}. Please enter a valid float.")
            elif isinstance(value, int):
                try:
                    updated_dict[key] = int(new_value)
                except ValueError:
                    st.error(f"Invalid input for {unique_key}. Please enter a valid integer.")
            else:
                # Assuming other types are strings
                updated_dict[key] = new_value
    return updated_dict

def update_room_program_types(hb_model, vintage, building_type):
    room_prog = filter_array_by_keywords(PROGRAM_TYPES, [vintage, building_type], False)
    for room in hb_model.rooms:
        if 'room_prog' not in room.user_data or room.user_data['room_prog'] not in room_prog:
            room.user_data['room_prog'] = random.choice(room_prog)
            room.properties.energy.program_type = program_type_by_identifier(room.user_data['room_prog'])

def iterate_rooms_and_display_properties():
    """Iterates through rooms in a Honeybee model, displaying and allowing the modification of various properties such as lighting, 
    people gains, equipment gains, service hot water, infiltration, ventilation, and setpoints. It requires a valid Honeybee model object 
    stored in the session state and uses Streamlit UI elements to interactively display and update room properties based on user input.
    
    The function first checks if the provided model is a valid Honeybee Model object. Then, it allows the user to select construction 
    period and building type from predefined lists, which are used to filter applicable room programs. Each room's properties are 
    displayed within a Streamlit expander, allowing for modifications to attributes such as display name, room program, and various 
    gains (lighting, people, electric equipment, gas equipment, service hot water, infiltration, and ventilation). The modifications are 
    applied to the model in real-time, enabling dynamic updates based on user interaction.
    
    Parameters: None
    Returns: None - This function directly modifies the session state and uses Streamlit components to display UI elements. """
    
    # Check if the 'hb_model' in the Streamlit session state is an instance of the Model class.
    # This is important because the operations that follow are specific to objects of the Model class.
    # If 'hb_model' is not a Model instance, it displays an error message and stops executing the function.
    if not isinstance(st.session_state.hb_model, Model):
        st.error("Invalid input. Please provide a valid Honeybee model object.")
        return

    # Use Streamlit's 'selectbox' to create a dropdown menu for selecting a construction period.
    # 'STANDARDS_REGISTRY' is a list containing different construction periods. The user's selection is stored in 'st.session_state.vintage'.
    # The '6' at the end specifies the default selection index from the 'STANDARDS_REGISTRY' list, making the seventh item the default choice.
    st.session_state.vintage = st.selectbox('Construction Period:', list(STANDARDS_REGISTRY), 6)
    
    # Similarly, create another dropdown menu for selecting a building type.
    # 'BUILDING_TYPES' is a list of different types of buildings. The user's selection is stored in 'st.session_state.building_type'.
    # Again, '6' is the default selection index, making the seventh item in the 'BUILDING_TYPES' list the default choice.
    st.session_state.building_type = st.selectbox('Building Type:', list(BUILDING_TYPES), 6)

    # Filter room programs based on the selected construction period and building type.
    # 'filter_array_by_keywords' is a function that likely takes a list of items ('PROGRAM_TYPES') and a list of keywords (selected vintage and building type)
    # and returns a subset of 'PROGRAM_TYPES' that match the keywords. The 'False' parameter might control the filtering behavior or case sensitivity.
    room_prog = filter_array_by_keywords(PROGRAM_TYPES, [st.session_state.vintage, st.session_state.building_type], False)
    
    # Iterate over each room in the Honeybee model.
    # 'st.session_state.hb_model.rooms' contains a list of rooms in the model. For each room, various properties will be displayed and can be modified.
    # Display each room's properties using expanders.
    for room in st.session_state.hb_model.rooms:
        with st.expander(f"Room identifier: {room.identifier}"):
            st.write("Floor area")
            st.code(room.floor_area)

            # Create a text input field for editing the room's display name.
            # A unique key for the input field is generated using the room's identifier to ensure that the input field's state is maintained uniquely across different rooms.
            room.display_name = st.text_input(f"Display name for {room.identifier}", value=room.display_name, key=f"display_name_{room.identifier}")

            # Generate a unique key for the room program selectbox using the room's identifier.
            # This ensures that each selectbox in the loop is treated as a distinct widget by Streamlit.
            selectbox_key = f"room_prog_{room.identifier}"
            # Determine the current index of the room's program type in the 'room_prog' list to set it as the default selection in the selectbox.
            # If the room's program type identifier is not in 'room_prog', default to the first item (index 0).
            current_prog_index = room_prog.index(room.properties.energy.program_type.identifier) if room.properties.energy.program_type.identifier in room_prog else 0
            # Create a selectbox for changing the room's program type, with the current program type pre-selected.
            new_room_prog = st.selectbox("Room Program", room_prog, index=current_prog_index, key=selectbox_key)
            
            # Check if the user has selected a different program type from the dropdown.
            # If so, update the room's program type to the new selection. Otherwise, keep it unchanged.
            if new_room_prog != room.properties.energy.program_type.identifier:
                new_program_type = program_type_by_identifier(new_room_prog)
                room.properties.energy.program_type = new_program_type
            else:
                # Duplicate the program type to ensure any modifications are made on a new instance, preserving the original object's state.
                new_program_type = room.properties.energy.program_type
            
            new_program_type = room.properties.energy.program_type.duplicate()
            
            # Check if the new program type has a lighting object associated with it.
            if new_program_type.lighting:
                st.divider() # Add a visual divider in the Streamlit interface to separate this section.
                st.write("Lighting gains") # Display a header or title for this section.
                # Duplicate the lighting object from the new program type. This is done to avoid modifying the original object directly.
                # Modifying a duplicate allows changes to be made safely without affecting other parts of the program that might be using the original object.
                lighting = new_program_type.lighting.duplicate()  # Duplicate the lighting object
                # Convert the lighting object's properties to a dictionary for easier manipulation.
                # This allows us to access and modify its properties as key-value pairs, which is more straightforward than dealing with the object's methods and attributes directly.
                lighting_dict = lighting.to_dict()
                # Update the lighting properties based on user input or some other logic.
                # 'update_properties_dict' is a function that takes the room object, the current lighting properties as a dictionary, and a string indicating the type of properties being updated ("lighting").
                # This function modify the properties based on user input collected elsewhere in the application.
                updated_lighting_dict = update_properties_dict(room, lighting_dict, "lighting")
                # Check if 'watts_per_area' is a key in the updated dictionary of lighting properties.
                # If it is, update the 'watts_per_area' property of the lighting object with the new value.
                if 'watts_per_area' in updated_lighting_dict:
                    lighting.watts_per_area = updated_lighting_dict['watts_per_area']
                if 'return_air_fraction' in updated_lighting_dict:
                    lighting.return_air_fraction = updated_lighting_dict['return_air_fraction']
                if 'radiant_fraction' in updated_lighting_dict:
                    lighting.radiant_fraction = updated_lighting_dict['radiant_fraction']
                if 'visible_fraction' in updated_lighting_dict:
                    lighting.visible_fraction = updated_lighting_dict['visible_fraction']
                if 'baseline_watts_per_area' in updated_lighting_dict:
                    lighting.baseline_watts_per_area = updated_lighting_dict['baseline_watts_per_area']
                
                # After updating the lighting object with new properties, assign it back to the new program type.
                # This ensures that the program type uses the updated lighting configuration.
                new_program_type.lighting = lighting

            if new_program_type.people:
                st.divider()
                st.write("People gains")
                people = new_program_type.people.duplicate()  # Duplicate the people object
                people_dict = people.to_dict()
                updated_people_dict = update_properties_dict(room, people_dict, "people")

                if 'people_per_area' in updated_people_dict:
                    people.people_per_area = updated_people_dict['people_per_area']
                if 'radiant_fraction' in updated_people_dict:
                    people.radiant_fraction = updated_people_dict['radiant_fraction']
                
                new_program_type.people = people

                if new_program_type.electric_equipment:
                    st.divider()
                    st.write("electric_equipment gains")
                    electric_equipment = new_program_type.electric_equipment.duplicate()  # Duplicate the electric_equipment object
                    electric_equipment_dict = electric_equipment.to_dict()
                    updated_electric_equipment_dict = update_properties_dict(room, electric_equipment_dict, "electric_equipment")

                    if 'watts_per_area' in updated_electric_equipment_dict:
                        electric_equipment.watts_per_area = updated_electric_equipment_dict['watts_per_area']
                    if 'radiant_fraction' in updated_electric_equipment_dict:
                        electric_equipment.radiant_fraction = updated_electric_equipment_dict['radiant_fraction']
                    if 'latent_fraction' in updated_electric_equipment_dict:
                        electric_equipment.latent_fraction = updated_electric_equipment_dict['latent_fraction']
                    if 'lost_fraction' in updated_electric_equipment_dict:
                        electric_equipment.lost_fraction = updated_electric_equipment_dict['lost_fraction']
                   
                    new_program_type.electric_equipment = electric_equipment
           
            if new_program_type.gas_equipment:
                st.divider()
                st.write("gas_equipment gains")
                gas_equipment = new_program_type.gas_equipment.duplicate()  # Duplicate the gas_equipment object
                gas_equipment_dict = gas_equipment.to_dict()
                updated_gas_equipment_dict = update_properties_dict(room, gas_equipment_dict, "gas_equipment")

                if 'watts_per_area' in updated_gas_equipment_dict:
                    gas_equipment.watts_per_area = updated_gas_equipment_dict['watts_per_area']
                if 'radiant_fraction' in updated_gas_equipment_dict:
                    gas_equipment.radiant_fraction = updated_gas_equipment_dict['radiant_fraction']
                if 'latent_fraction' in updated_gas_equipment_dict:
                    gas_equipment.latent_fraction = updated_gas_equipment_dict['latent_fraction']
                if 'lost_fraction' in updated_gas_equipment_dict:
                    gas_equipment.lost_fraction = updated_gas_equipment_dict['lost_fraction']

                
                new_program_type.gas_equipment = gas_equipment

            if new_program_type.service_hot_water:
                st.divider()
                st.write("service_hot_water gains")
                service_hot_water = new_program_type.service_hot_water.duplicate()  # Duplicate the service_hot_water object
                service_hot_water_dict = service_hot_water.to_dict()
                updated_service_hot_water_dict = update_properties_dict(room, service_hot_water_dict, "service_hot_water")

                if 'service_hot_water_per_area' in updated_service_hot_water_dict:
                    service_hot_water.service_hot_water_per_area = updated_service_hot_water_dict['service_hot_water_per_area']
                if 'flow_per_area' in updated_service_hot_water_dict:
                    service_hot_water.flow_per_area = updated_service_hot_water_dict['flow_per_area']
                if 'target_temperature' in updated_service_hot_water_dict:
                    service_hot_water.target_temperature = updated_service_hot_water_dict['target_temperature']
                if 'sensible_fraction' in updated_service_hot_water_dict:
                    service_hot_water.sensible_fraction = updated_service_hot_water_dict['sensible_fraction']
                if 'latent_fraction' in updated_service_hot_water_dict:
                    service_hot_water.latent_fraction = updated_service_hot_water_dict['latent_fraction']
                
                new_program_type.service_hot_water = service_hot_water

            if new_program_type.infiltration:
                st.divider()
                st.write("infiltration gains")
                infiltration = new_program_type.infiltration.duplicate()  # Duplicate the infiltration object
                infiltration_dict = infiltration.to_dict()
                updated_infiltration_dict = update_properties_dict(room, infiltration_dict, "infiltration")

                if 'flow_per_exterior_area' in updated_infiltration_dict:
                    infiltration.flow_per_exterior_area = updated_infiltration_dict['flow_per_exterior_area']
                new_program_type.infiltration = infiltration    
            
            if new_program_type.ventilation:
                st.divider()
                st.write("ventilation gains")
                ventilation = new_program_type.ventilation.duplicate()  # Duplicate the ventilation object
                ventilation_dict = ventilation.to_dict()
                updated_ventilation_dict = update_properties_dict(room, ventilation_dict, "ventilation")

                if 'flow_per_person' in updated_ventilation_dict:
                    ventilation.flow_per_person = updated_ventilation_dict['flow_per_person']
                if 'flow_per_area' in updated_ventilation_dict:
                    ventilation.flow_per_area = updated_ventilation_dict['flow_per_area']
                
                new_program_type.ventilation = ventilation
            
            if new_program_type.setpoint:
                st.divider()
                st.write("setpoint gains")
                setpoint = new_program_type.setpoint.duplicate()  # Duplicate the setpoint object
                setpoint_dict = setpoint.to_dict()
                updated_setpoint_dict = update_properties_dict(room, setpoint_dict, "setpoint")

                if 'setpoint_per_area' in updated_setpoint_dict:
                    setpoint.setpoint_per_area = updated_setpoint_dict['setpoint_per_area']
                
                new_program_type.setpoint = setpoint

            # Assign the updated lighting object back to the new ProgramType
            room.properties.energy.program_type = new_program_type

