from honeybee_energy.altnumber import Autosize
from honeybee.altnumber import NoLimit
# all air
from honeybee_energy.hvac.allair.furnace import ForcedAirFurnace
from honeybee_energy.hvac.allair.psz import PSZ
from honeybee_energy.hvac.allair.ptac import PTAC
from honeybee_energy.hvac.allair.pvav import PVAV
from honeybee_energy.hvac.allair.vav import VAV
# DOAS
from honeybee_energy.hvac.doas.fcu import FCUwithDOAS
from honeybee_energy.hvac.doas.radiant import RadiantwithDOAS
from honeybee_energy.hvac.doas.vrf import VRFwithDOAS
from honeybee_energy.hvac.doas.wshp import WSHPwithDOAS
# Heatcool
from honeybee_energy.hvac.heatcool.baseboard import Baseboard
from honeybee_energy.hvac.heatcool.evapcool import EvaporativeCooler
from honeybee_energy.hvac.heatcool.radiant import Radiant
from honeybee_energy.hvac.heatcool.fcu import FCU
from honeybee_energy.hvac.heatcool.gasunit import GasUnitHeater
from honeybee_energy.hvac.heatcool.residential import Residential
from honeybee_energy.hvac.heatcool.vrf import VRF
from honeybee_energy.hvac.heatcool.windowac import WindowAC
from honeybee_energy.hvac.heatcool.wshp import WSHP
# Ideal Air system
from honeybee_energy.hvac.idealair import IdealAirSystem
# Model
from honeybee.model import Model,Room
import uuid

ROOM_EQUIPMENT= ("ForcedAirFurnace","PSZ","PTAC","PVAV","VAV","FCUwithDOAS","RadiantwithDOAS","VRFwithDOAS","WSHPwithDOAS","Baseboard","EvaporativeCooler",
            "FCU","GasUnitHeater","Radiant","Residential","VRF","WindowAC","WSHP", 'IdealAirSystem', "Not Conditioned")

def get_ForcedAirFurnace(st, room):
    from honeybee_energy.hvac.allair.furnace import ForcedAirFurnace

    # Instantiate the ForcedAirFurnace system with a unique identifier
    identifier = f"ForcedAirFurnace-{room.identifier}"
    standard_system = ForcedAirFurnace(identifier)
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(standard_system.vintage), key=f"vintage-{room.identifier}")
    standard_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['Furnace', 'Furnace_Electric']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(standard_system.equipment_type if standard_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    standard_system.equipment_type = equipment_type

    # Selectbox for economizer_type
    economizer_type_options = ['NoEconomizer', 'DifferentialDryBulb', 'DifferentialEnthalpy', 'DifferentialDryBulbAndEnthalpy', 'FixedDryBulb', 'FixedEnthalpy', 'ElectronicEnthalpy']
    economizer_type = st.selectbox("Economizer Type", options=economizer_type_options, index=economizer_type_options.index(standard_system.economizer_type), key=f"economizer_type-{room.identifier}")
    standard_system.economizer_type = economizer_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(standard_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    standard_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(standard_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    standard_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=float(standard_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    standard_system.demand_controlled_ventilation = demand_controlled_ventilation

    return standard_system

def get_PSZSystem(st, room):
    from honeybee_energy.hvac.allair.psz import PSZ
    unique_key_suffix = uuid.uuid4().hex[:8]
    # Instantiate the PSZ system with a unique identifier
    identifier = f"PSZ-{room.identifier}"
    psz_system = PSZ(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(psz_system.vintage), key=f"vintage-{room.identifier}")
    psz_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['PSZAC_ElectricBaseboard', 'PSZAC_BoilerBaseboard', 'PSZAC_DHWBaseboard', 'PSZAC_GasHeaters', 'PSZAC_ElectricCoil', 'PSZAC_GasCoil', 'PSZAC_Boiler', 'PSZAC_ASHP', 'PSZAC_DHW', 'PSZAC', 'PSZAC_DCW_ElectricBaseboard', 'PSZAC_DCW_BoilerBaseboard', 'PSZAC_DCW_GasHeaters', 'PSZAC_DCW_ElectricCoil', 'PSZAC_DCW_GasCoil', 'PSZAC_DCW_Boiler', 'PSZAC_DCW_ASHP', 'PSZAC_DCW_DHW', 'PSZAC_DCW', 'PSZHP']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(psz_system.equipment_type if psz_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    psz_system.equipment_type = equipment_type

    # Selectbox for economizer_type
    economizer_type_options = ['NoEconomizer', 'DifferentialDryBulb', 'DifferentialEnthalpy', 'DifferentialDryBulbAndEnthalpy', 'FixedDryBulb', 'FixedEnthalpy', 'ElectronicEnthalpy']
    economizer_type = st.selectbox("Economizer Type", options=economizer_type_options, index=economizer_type_options.index(psz_system.economizer_type), key=f"economizer_type-{room.identifier}")
    psz_system.economizer_type = economizer_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(psz_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    psz_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(psz_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    psz_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(psz_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    psz_system.demand_controlled_ventilation = demand_controlled_ventilation

    return psz_system

def get_PTACSystem(st, room):
    from honeybee_energy.hvac.allair.ptac import PTAC
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the PTAC system with a unique identifier
    identifier = f"PTAC-{room.identifier}"
    ptac_system = PTAC(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(ptac_system.vintage), key=f"vintage-{room.identifier}")
    ptac_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['PTAC_ElectricBaseboard', 'PTAC_BoilerBaseboard', 'PTAC_DHWBaseboard', 'PTAC_GasHeaters', 'PTAC_ElectricCoil', 'PTAC_GasCoil', 'PTAC_Boiler', 'PTAC_ASHP', 'PTAC_DHW', 'PTAC', 'PTHP']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(ptac_system.equipment_type if ptac_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    ptac_system.equipment_type = equipment_type

    return ptac_system

def get_PVAVSystem(st, room):
    from honeybee_energy.hvac.allair.pvav import PVAV
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the PVAV system with a unique identifier
    identifier = f"PVAV-{room.identifier}"
    pvav_system = PVAV(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(pvav_system.vintage), key=f"vintage-{room.identifier}")
    pvav_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['PVAV_Boiler', 'PVAV_ASHP', 'PVAV_DHW', 'PVAV_PFP', 'PVAV_BoilerElectricReheat']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(pvav_system.equipment_type if pvav_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    pvav_system.equipment_type = equipment_type

    # Selectbox for economizer_type
    economizer_type_options = ['NoEconomizer', 'DifferentialDryBulb', 'DifferentialEnthalpy', 'DifferentialDryBulbAndEnthalpy', 'FixedDryBulb', 'FixedEnthalpy', 'ElectronicEnthalpy']
    economizer_type = st.selectbox("Economizer Type", options=economizer_type_options, index=economizer_type_options.index(pvav_system.economizer_type), key=f"economizer_type-{room.identifier}")
    pvav_system.economizer_type = economizer_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(pvav_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    pvav_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(pvav_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    pvav_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(pvav_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    pvav_system.demand_controlled_ventilation = demand_controlled_ventilation

    return pvav_system

def get_VAVSystem(st, room):
    from honeybee_energy.hvac.allair.vav import VAV
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the VAV system with a unique identifier
    identifier = f"VAV-{room.identifier}"
    vav_system = VAV(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(vav_system.vintage), key=f"vintage-{room.identifier}")
    vav_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['VAV_Chiller_Boiler', 'VAV_Chiller_ASHP', 'VAV_Chiller_DHW', 'VAV_Chiller_PFP', 'VAV_Chiller_GasCoil', 'VAV_ACChiller_Boiler', 'VAV_ACChiller_ASHP', 'VAV_ACChiller_DHW', 'VAV_ACChiller_PFP', 'VAV_ACChiller_GasCoil', 'VAV_DCW_Boiler', 'VAV_DCW_ASHP', 'VAV_DCW_DHW', 'VAV_DCW_PFP', 'VAV_DCW_GasCoil']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(vav_system.equipment_type if vav_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    vav_system.equipment_type = equipment_type

    # Selectbox for economizer_type
    economizer_type_options = ['NoEconomizer', 'DifferentialDryBulb', 'DifferentialEnthalpy', 'DifferentialDryBulbAndEnthalpy', 'FixedDryBulb', 'FixedEnthalpy', 'ElectronicEnthalpy']
    economizer_type = st.selectbox("Economizer Type", options=economizer_type_options, index=economizer_type_options.index(vav_system.economizer_type), key=f"economizer_type-{room.identifier}")
    vav_system.economizer_type = economizer_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(vav_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    vav_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(vav_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    vav_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(vav_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    vav_system.demand_controlled_ventilation = demand_controlled_ventilation

    return vav_system

def get_FCUwithDOASSystem(st, room):
    from honeybee_energy.hvac.doas.fcu import FCUwithDOAS
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the FCUwithDOAS system with a unique identifier
    identifier = f"FCUwithDOAS-{room.identifier}"
    fcuwithdoas_system = FCUwithDOAS(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(fcuwithdoas_system.vintage), key=f"vintage-{room.identifier}")
    fcuwithdoas_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'DOAS_FCU_Chiller_Boiler', 'DOAS_FCU_Chiller_ASHP', 'DOAS_FCU_Chiller_DHW',
        'DOAS_FCU_Chiller_ElectricBaseboard', 'DOAS_FCU_Chiller_GasHeaters', 'DOAS_FCU_Chiller',
        'DOAS_FCU_ACChiller_Boiler', 'DOAS_FCU_ACChiller_ASHP', 'DOAS_FCU_ACChiller_DHW',
        'DOAS_FCU_ACChiller_ElectricBaseboard', 'DOAS_FCU_ACChiller_GasHeaters', 'DOAS_FCU_ACChiller',
        'DOAS_FCU_DCW_Boiler', 'DOAS_FCU_DCW_ASHP', 'DOAS_FCU_DCW_DHW',
        'DOAS_FCU_DCW_ElectricBaseboard', 'DOAS_FCU_DCW_GasHeaters', 'DOAS_FCU_DCW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(fcuwithdoas_system.equipment_type if fcuwithdoas_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    fcuwithdoas_system.equipment_type = equipment_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(fcuwithdoas_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    fcuwithdoas_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(fcuwithdoas_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    fcuwithdoas_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(fcuwithdoas_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    fcuwithdoas_system.demand_controlled_ventilation = demand_controlled_ventilation

    # Text_input for doas_availability_schedule
    # This is an optional schedule. You may need to adjust the implementation based on how you manage schedules in your app.
    # Here's a simplistic approach to accept a string, assuming users enter a valid schedule name or None.
    doas_availability_schedule = st.text_input("DOAS Availability Schedule (optional)", key=f"doas_availability_schedule-{room.identifier}")
    fcuwithdoas_system.doas_availability_schedule = doas_availability_schedule if doas_availability_schedule != '' else None

    return fcuwithdoas_system

def get_VRFwithDOASSystem(st, room):
    from honeybee_energy.hvac.doas.vrf import VRFwithDOAS
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the VRFwithDOAS system with a unique identifier
    identifier = f"VRFwithDOAS-{room.identifier}"
    vrfwithdoas_system = VRFwithDOAS(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(vrfwithdoas_system.vintage), key=f"vintage-{room.identifier}")
    vrfwithdoas_system.vintage = vintage

    # Equipment type for VRF with DOAS is not selectable as there is only one option provided in the parameters.
    # Assuming 'DOAS_VRF' is the default and only equipment type.
    vrfwithdoas_system.equipment_type = 'DOAS_VRF'

    # Display the fixed equipment type to the user
    st.text(f"Equipment Type: {vrfwithdoas_system.equipment_type}")

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(vrfwithdoas_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    vrfwithdoas_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(vrfwithdoas_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    vrfwithdoas_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(vrfwithdoas_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    vrfwithdoas_system.demand_controlled_ventilation = demand_controlled_ventilation

    # Text_input for doas_availability_schedule
    # This is an optional schedule. Implementation depends on how you manage schedules in your app.
    doas_availability_schedule = st.text_input("DOAS Availability Schedule (optional)", key=f"doas_availability_schedule-{room.identifier}")
    vrfwithdoas_system.doas_availability_schedule = doas_availability_schedule if doas_availability_schedule != '' else None

    return vrfwithdoas_system

def get_RadiantwithDOASSystem(st, room):
    from honeybee_energy.hvac.doas.radiant import RadiantwithDOAS
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the RadiantwithDOAS system with a unique identifier
    identifier = f"RadiantwithDOAS-{room.identifier}"
    radiantwithdoas_system = RadiantwithDOAS(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(radiantwithdoas_system.vintage), key=f"vintage-{room.identifier}")
    radiantwithdoas_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'DOAS_Radiant_Chiller_Boiler', 'DOAS_Radiant_Chiller_ASHP', 'DOAS_Radiant_Chiller_DHW',
        'DOAS_Radiant_ACChiller_Boiler', 'DOAS_Radiant_ACChiller_ASHP', 'DOAS_Radiant_ACChiller_DHW',
        'DOAS_Radiant_DCW_Boiler', 'DOAS_Radiant_DCW_ASHP', 'DOAS_Radiant_DCW_DHW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(radiantwithdoas_system.equipment_type if radiantwithdoas_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    radiantwithdoas_system.equipment_type = equipment_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(radiantwithdoas_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    radiantwithdoas_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(radiantwithdoas_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    radiantwithdoas_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(radiantwithdoas_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    radiantwithdoas_system.demand_controlled_ventilation = demand_controlled_ventilation

    # Text_input for doas_availability_schedule
    doas_availability_schedule = st.text_input("DOAS Availability Schedule (optional)", key=f"doas_availability_schedule-{room.identifier}")
    radiantwithdoas_system.doas_availability_schedule = doas_availability_schedule if doas_availability_schedule != '' else None

    # Selectbox for radiant_type
    radiant_type_options = ['Floor', 'Ceiling', 'FloorWithCarpet', 'CeilingMetalPanel', 'FloorWithHardwood']
    radiant_type = st.selectbox("Radiant Type", options=radiant_type_options, index=radiant_type_options.index(radiantwithdoas_system.radiant_type), key=f"radiant_type-{room.identifier}")
    radiantwithdoas_system.radiant_type = radiant_type

    # Number_input for minimum_operation_time
    minimum_operation_time = st.number_input("Minimum Operation Time", min_value=1, value=int(radiantwithdoas_system.minimum_operation_time), step=1, key=f"minimum_operation_time-{room.identifier}")
    radiantwithdoas_system.minimum_operation_time = minimum_operation_time

    # Number_input for switch_over_time
    switch_over_time = st.number_input("Switch Over Time", min_value=1, value=int(radiantwithdoas_system.switch_over_time), step=1, key=f"switch_over_time-{room.identifier}")
    radiantwithdoas_system.switch_over_time = switch_over_time

    return radiantwithdoas_system

def get_WSHPwithDOASSystem(st, room):
    from honeybee_energy.hvac.doas.wshp import WSHPwithDOAS
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the WSHPwithDOAS system with a unique identifier
    identifier = f"WSHPwithDOAS-{room.identifier}"
    wshpwithdoas_system = WSHPwithDOAS(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(wshpwithdoas_system.vintage), key=f"vintage-{room.identifier}")
    wshpwithdoas_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'DOAS_WSHP_FluidCooler_Boiler', 'DOAS_WSHP_CoolingTower_Boiler', 'DOAS_WSHP_GSHP', 'DOAS_WSHP_DCW_DHW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(wshpwithdoas_system.equipment_type if wshpwithdoas_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    wshpwithdoas_system.equipment_type = equipment_type

    # Number_input for sensible_heat_recovery
    sensible_heat_recovery = st.number_input("Sensible Heat Recovery", min_value=0.0, max_value=1.0, value=float(wshpwithdoas_system.sensible_heat_recovery), step=0.01, key=f"sensible_heat_recovery-{room.identifier}")
    wshpwithdoas_system.sensible_heat_recovery = sensible_heat_recovery

    # Number_input for latent_heat_recovery
    latent_heat_recovery = st.number_input("Latent Heat Recovery", min_value=0.0, max_value=1.0, value=float(wshpwithdoas_system.latent_heat_recovery), step=0.01, key=f"latent_heat_recovery-{room.identifier}")
    wshpwithdoas_system.latent_heat_recovery = latent_heat_recovery

    # Checkbox for demand_controlled_ventilation
    demand_controlled_ventilation = st.checkbox("Demand Controlled Ventilation", value=bool(wshpwithdoas_system.demand_controlled_ventilation), key=f"demand_controlled_ventilation-{room.identifier}")
    wshpwithdoas_system.demand_controlled_ventilation = demand_controlled_ventilation

    # Text_input for doas_availability_schedule
    doas_availability_schedule = st.text_input("DOAS Availability Schedule (optional)", key=f"doas_availability_schedule-{room.identifier}")
    wshpwithdoas_system.doas_availability_schedule = doas_availability_schedule if doas_availability_schedule != '' else None

    return wshpwithdoas_system

def get_BaseboardSystem(st, room):
    from honeybee_energy.hvac.heatcool.baseboard import Baseboard
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the Baseboard system with a unique identifier
    identifier = f"Baseboard-{room.identifier}"
    baseboard_system = Baseboard(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(baseboard_system.vintage), key=f"vintage-{room.identifier}")
    baseboard_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = ['ElectricBaseboard', 'BoilerBaseboard', 'ASHPBaseboard', 'DHWBaseboard']
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(baseboard_system.equipment_type if baseboard_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    baseboard_system.equipment_type = equipment_type

    return baseboard_system

def get_EvaporativeCoolerSystem(st, room):
    from honeybee_energy.hvac.heatcool.evapcool import EvaporativeCooler
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the EvaporativeCooler system with a unique identifier
    identifier = f"EvaporativeCooler-{room.identifier}"
    evaporative_cooler_system = EvaporativeCooler(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(evaporative_cooler_system.vintage), key=f"vintage-{room.identifier}")
    evaporative_cooler_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'EvapCoolers_ElectricBaseboard', 'EvapCoolers_BoilerBaseboard', 'EvapCoolers_ASHPBaseboard', 
        'EvapCoolers_DHWBaseboard', 'EvapCoolers_Furnace', 'EvapCoolers_UnitHeaters', 'EvapCoolers'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(evaporative_cooler_system.equipment_type if evaporative_cooler_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    evaporative_cooler_system.equipment_type = equipment_type

    return evaporative_cooler_system

def get_FCUSystem(st, room):
    from honeybee_energy.hvac.heatcool.fcu import FCU
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the FCU system with a unique identifier
    identifier = f"FCU-{room.identifier}"
    fcu_system = FCU(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(fcu_system.vintage), key=f"vintage-{room.identifier}")
    fcu_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'FCU_Chiller_Boiler', 'FCU_Chiller_ASHP', 'FCU_Chiller_DHW', 'FCU_Chiller_ElectricBaseboard', 
        'FCU_Chiller_GasHeaters', 'FCU_Chiller', 'FCU_ACChiller_Boiler', 'FCU_ACChiller_ASHP', 
        'FCU_ACChiller_DHW', 'FCU_ACChiller_ElectricBaseboard', 'FCU_ACChiller_GasHeaters', 
        'FCU_ACChiller', 'FCU_DCW_Boiler', 'FCU_DCW_ASHP', 'FCU_DCW_DHW', 'FCU_DCW_ElectricBaseboard', 
        'FCU_DCW_GasHeaters', 'FCU_DCW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(fcu_system.equipment_type if fcu_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    fcu_system.equipment_type = equipment_type

    return fcu_system

def get_GasUnitHeaterSystem(st, room):
    from honeybee_energy.hvac.heatcool.gasunit import GasUnitHeater
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the GasUnitHeater system with a unique identifier
    identifier = f"GasUnitHeater-{room.identifier}"
    gas_unit_heater_system = GasUnitHeater(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(gas_unit_heater_system.vintage), key=f"vintage-{room.identifier}")
    gas_unit_heater_system.vintage = vintage

    # The Gas Unit Heater system has a single equipment type option 'GasHeaters'.
    # Assuming 'GasHeaters' is the default and only equipment type.
    gas_unit_heater_system.equipment_type = 'GasHeaters'

    # Display the fixed equipment type to the user
    st.text(f"Equipment Type: {gas_unit_heater_system.equipment_type}")

    return gas_unit_heater_system

def get_RadiantSystem(st, room):
    from honeybee_energy.hvac.heatcool.radiant import Radiant
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the Radiant system with a unique identifier
    identifier = f"Radiant-{room.identifier}"
    radiant_system = Radiant(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(radiant_system.vintage), key=f"vintage-{room.identifier}")
    radiant_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'Radiant_Chiller_Boiler', 'Radiant_Chiller_ASHP', 'Radiant_Chiller_DHW', 
        'Radiant_ACChiller_Boiler', 'Radiant_ACChiller_ASHP', 'Radiant_ACChiller_DHW', 
        'Radiant_DCW_Boiler', 'Radiant_DCW_ASHP', 'Radiant_DCW_DHW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(radiant_system.equipment_type if radiant_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    radiant_system.equipment_type = equipment_type

    # Selectbox for radiant_type
    radiant_type_options = ['Floor', 'Ceiling', 'FloorWithCarpet', 'CeilingMetalPanel', 'FloorWithHardwood']
    radiant_type = st.selectbox("Radiant Type", options=radiant_type_options, index=radiant_type_options.index(radiant_system.radiant_type), key=f"radiant_type-{room.identifier}")
    radiant_system.radiant_type = radiant_type

    # Number_input for minimum_operation_time
    minimum_operation_time = st.number_input("Minimum Operation Time", min_value=1, value=int(radiant_system.minimum_operation_time), step=1, key=f"minimum_operation_time-{room.identifier}")
    radiant_system.minimum_operation_time = minimum_operation_time

    # Number_input for switch_over_time
    switch_over_time = st.number_input("Switch Over Time", min_value=1, value=int(radiant_system.switch_over_time), step=1, key=f"switch_over_time-{room.identifier}")
    radiant_system.switch_over_time = switch_over_time

    return radiant_system

def get_VRFSystem(st, room):
    from honeybee_energy.hvac.heatcool.vrf import VRF
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the VRF system with a unique identifier
    identifier = f"VRF-{room.identifier}"
    vrf_system = VRF(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(vrf_system.vintage), key=f"vintage-{room.identifier}")
    vrf_system.vintage = vintage

    # The VRF system has a single equipment type option 'VRF'.
    # Assuming 'VRF' is the default and only equipment type.
    vrf_system.equipment_type = 'VRF'

    # Display the fixed equipment type to the user
    st.text(f"Equipment Type: {vrf_system.equipment_type}")

    return vrf_system

def get_WindowACSystem(st, room):
    from honeybee_energy.hvac.heatcool.windowac import WindowAC
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the WindowAC system with a unique identifier
    identifier = f"WindowAC-{room.identifier}"
    window_ac_system = WindowAC(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(window_ac_system.vintage), key=f"vintage-{room.identifier}")
    window_ac_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'WindowAC_ElectricBaseboard', 'WindowAC_BoilerBaseboard', 'WindowAC_ASHPBaseboard', 
        'WindowAC_DHWBaseboard', 'WindowAC_Furnace', 'WindowAC_GasHeaters', 'WindowAC'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(window_ac_system.equipment_type if window_ac_system.equipment_type else equipment_type_options[-1]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    window_ac_system.equipment_type = equipment_type

    return window_ac_system

def get_WSHPSystem(st, room):
    from honeybee_energy.hvac.heatcool.wshp import WSHP
    unique_key_suffix = uuid.uuid4().hex[:8]  # Take first 8 characters for brevity

    # Instantiate the WSHP system with a unique identifier
    identifier = f"WSHP-{room.identifier}"
    wshp_system = WSHP(identifier)

    # Selectbox for vintage
    vintage_options = ['DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019']
    vintage = st.selectbox("Vintage", options=vintage_options, index=vintage_options.index(wshp_system.vintage), key=f"vintage-{room.identifier}")
    wshp_system.vintage = vintage

    # Selectbox for equipment_type
    equipment_type_options = [
        'WSHP_FluidCooler_Boiler', 'WSHP_CoolingTower_Boiler', 'WSHP_GSHP', 'WSHP_DCW_DHW'
    ]
    equipment_type = st.selectbox("Equipment Type", options=equipment_type_options, index=equipment_type_options.index(wshp_system.equipment_type if wshp_system.equipment_type else equipment_type_options[0]), key=f"equipment_subtype-{room.identifier}-{unique_key_suffix}")
    wshp_system.equipment_type = equipment_type

    return wshp_system

def assign_hvac_system(st, room, equipment_type):
    if equipment_type == "ForcedAirFurnace":
        room.properties.energy.hvac = get_ForcedAirFurnace(st, room)
    elif equipment_type == "PSZ":
        room.properties.energy.hvac = get_PSZSystem(st, room)
    elif equipment_type == "PTAC":
        room.properties.energy.hvac = get_PTACSystem(st, room)
    elif equipment_type == "PVAV":
        room.properties.energy.hvac = get_PVAVSystem(st, room)
    elif equipment_type == "VAV":
        room.properties.energy.hvac = get_VAVSystem(st, room)
    elif equipment_type == "FCUwithDOAS":
        room.properties.energy.hvac = get_FCUwithDOASSystem(st, room)
    elif equipment_type == "VRFwithDOAS":
        room.properties.energy.hvac = get_VRFwithDOASSystem(st, room)
    elif equipment_type == "RadiantwithDOAS":
        room.properties.energy.hvac = get_RadiantwithDOASSystem(st, room)
    elif equipment_type == "WSHPwithDOAS":
        room.properties.energy.hvac = get_WSHPwithDOASSystem(st, room)
    elif equipment_type == "Baseboard":
        room.properties.energy.hvac = get_BaseboardSystem(st, room)
    elif equipment_type == "EvaporativeCooler":
        room.properties.energy.hvac = get_EvaporativeCoolerSystem(st, room)
    elif equipment_type == "FCU":
        room.properties.energy.hvac = get_FCUSystem(st, room)
    elif equipment_type == "GasUnitHeater":
        room.properties.energy.hvac = get_GasUnitHeaterSystem(st, room)
    elif equipment_type == "Radiant":
        room.properties.energy.hvac = get_RadiantSystem(st, room)
    elif equipment_type == "VRF":
        room.properties.energy.hvac = get_VRFSystem(st, room)
    elif equipment_type == "WindowAC":
        room.properties.energy.hvac = get_WindowACSystem(st, room)
    elif equipment_type == "WSHP":
        room.properties.energy.hvac = get_WSHPSystem(st, room)

def iterate_rooms_hvac(tab,st):
    # Check if the 'hb_model' in the Streamlit session state is an instance of the Model class.
    # This is important because the operations that follow are specific to objects of the Model class.
    # If 'hb_model' is not a Model instance, it displays an error message and stops executing the function.
    if not isinstance(st.session_state.hb_model, Model):
        st.error("Invalid input. Please provide a valid Honeybee model object.")
        return
        
    for room in st.session_state.hb_model.rooms:
        with st.expander(f"Room identifier: {room.identifier}"):
            st.write("HVAC assigned")
            if room.properties.energy.hvac:
                attributes = room.properties.energy.hvac.to_dict()
            else:
                attributes = {"type": "IdealAirSystem"}
                
            equipment_type = st.selectbox("Equipment type", ROOM_EQUIPMENT,index=ROOM_EQUIPMENT.index(attributes["type"]),key=f"equipment_subtype-{room.identifier}")
            assign_hvac_system(st, room, equipment_type)