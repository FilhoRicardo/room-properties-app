
"""Streamlit application for creating and visualizing Room Properties.

This module defines the main application interface and logic for the Streamlit 
application. The application allows users to set parameters for a building's 
geometry, generates the corresponding building model, and provides an option 
to visualize the model.
"""

# Import necessary libraries and modules
import streamlit as st
from pathlib import Path
import tempfile
import json

# Import local modules for handling inputs and web visualization
from inputs import (initialize,upload_hbjson_file,iterate_rooms_and_display_properties)
import web as web

# Set the page configuration for Streamlit, defining the title
st.set_page_config(page_title="Room Properties App")

def main():
    """Main function for the Room Properties Streamlit App.
    
    This function orchestrates the user interface and interactions for the 
    Streamlit application. It initializes session state variables, displays 
    input sliders for users to set building parameters, generates the building 
    model based on those parameters, and provides an option to visualize the 
    model in 3D.
    """
    
    # Display application title and a separator
    st.header("Room Properties")
    st.markdown("---")
    
    # Initialize session state variables and settings for the application
    initialize()

    # Allow user to upload a Honeybee json file
    st.title("Honeybee JSON File Uploader")
    upload_hbjson_file()
    
   

    if st.session_state.hb_model:
        iterate_rooms_and_display_properties()
        st.text("Download model as HB Json file")
        # To download the model we need to convert the object into a string - this is called serialization
        json_string = json.dumps(st.session_state.hb_model.to_dict())
        st.download_button(label="Download HB Json",data=json_string,file_name="parametricModel.json",mime="application/json")
        

if __name__ == "__main__":
    # Run the main function if this module is executed as the main script
    main()
