from honeybee_energy.load.lighting import Lighting
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from honeybee_energy.load.people import People
from honeybee_energy.load.equipment import ElectricEquipment
from honeybee_energy.load.infiltration import Infiltration
import uuid

schedule_limits_dict = {
                "type": 'ScheduleTypeLimit',
                "identifier": 'Fractional',
                "display_name": 'Fractional',
                "lower_limit": 0,
                "upper_limit": 1,
                "numeric_type": 'Continuous',
                "unit_type": "Dimensionless"
                }

schedule_limits = ScheduleTypeLimit.from_dict(schedule_limits_dict)

schedule_default_day_dict = {
    "type": 'ScheduleDay',
    "identifier": 'Office_Occ_900_1700',
    "display_name": 'Office Occupancy',
    "values": [0, 1, 0],
    "times": [(0, 0), (9, 0), (17, 0)],
    "interpolate": False
}

schedule_off_day_dict = {
    "type": 'ScheduleDay',
    "identifier": 'Office_Occ_0000_0000',
    "display_name": 'Office Occupancy',
    "values": [0],
    "times": [(0, 0)],
    "interpolate": False
}

schedule_constant_one_dict = {
    "type": 'ScheduleDay',
    "identifier": 'Constant_On',
    "display_name": 'Constant On',
    "values": [1],
    "times": [(0, 0)],
    "interpolate": False
}


schedule_default_day = ScheduleDay.from_dict(schedule_default_day_dict)
schedule_off_day = ScheduleDay.from_dict(schedule_off_day_dict)
schedule_constant_one = ScheduleDay.from_dict(schedule_off_day_dict)

schedule_ruleset_dict = {
    "type": 'ScheduleRuleset',
    "identifier": 'Office_Occ_900_1700_weekends',
    "display_name": 'Office Occupancy',
    "day_schedules": [schedule_default_day.to_dict(),schedule_off_day.to_dict()], # Array of ScheduleDay dictionary representations
    "default_day_schedule": str(schedule_default_day.identifier), # ScheduleDay identifier
    "schedule_rules": [], # list of ScheduleRuleAbridged dictionaries
    "schedule_type_limit": schedule_limits.to_dict(), # ScheduleTypeLimit dictionary representation
    "holiday_schedule": str(schedule_default_day.identifier), # ScheduleDay identifier
    "summer_designday_schedule": str(schedule_off_day.identifier), # ScheduleDay identifier
    "winter_designday_schedule": str(schedule_off_day.identifier) # ScheduleDay identifier
}

ruleset_schedule = ScheduleRuleset.from_dict(schedule_ruleset_dict)

constant_on_schedule_ruleset_dict = {
    "type": 'ScheduleRuleset',
    "identifier": 'Constant_On',
    "display_name": 'Constant On',
    "day_schedules": [schedule_constant_one.to_dict()], # Array of ScheduleDay dictionary representations
    "default_day_schedule": str(schedule_constant_one.identifier), # ScheduleDay identifier
    "schedule_rules": [], # list of ScheduleRuleAbridged dictionaries
    "schedule_type_limit": schedule_limits.to_dict(), # ScheduleTypeLimit dictionary representation
    "holiday_schedule": str(schedule_constant_one.identifier), # ScheduleDay identifier
    "summer_designday_schedule": str(schedule_constant_one.identifier), # ScheduleDay identifier
    "winter_designday_schedule": str(schedule_constant_one.identifier) # ScheduleDay identifier
}

constant_on_ruleset_schedule = ScheduleRuleset.from_dict(constant_on_schedule_ruleset_dict)

def get_lighting_gains(room):

    lighting_dict = {
        "type": 'Lighting',
        "identifier": f'Lighting_{str(uuid.uuid4())[:8]}',
        "display_name": f'Lighting_{room.identifier}',
        "watts_per_area": 10, # lighting watts per square meter of floor area
        "schedule": ruleset_schedule.to_dict(), # ScheduleRuleset/ScheduleFixedInterval dictionary
        "return_air_fraction": 0, # fraction of heat going to return air
        "radiant_fraction": 0.32, # fraction of heat that is long wave radiant
        "visible_fraction": 0.25 # fraction of heat that is short wave visible
    }

    return Lighting.from_dict(lighting_dict)

def get_occupancy_gains(room):

    occupancy_dict = {
        "type": 'People',
        "identifier": f'Open_Office_People_{str(uuid.uuid4())[:8]}',
        "display_name": f'Office People {room.identifier}',
        "people_per_area": 0.05, # number of people per square meter of floor area
        "occupancy_schedule": ruleset_schedule.to_dict(), # ScheduleRuleset/ScheduleFixedInterval dictionary
        #"activity_schedule": {}, # ScheduleRuleset/ScheduleFixedInterval dictionary
        "radiant_fraction": 0.3, # fraction of sensible heat that is radiant
        "latent_fraction": 0.2 # fraction of total heat that is latent
    }

    return People.from_dict(occupancy_dict)

def get_elec_equip_gains(room):

    elec_equip_dict = {
    "type": 'ElectricEquipment',
    "identifier": f'Open_Office_Equipment_{str(uuid.uuid4())[:8]}',
    "display_name": f'Office Equipment {room.identifier}',
    "watts_per_area": 5, # equipment watts per square meter of floor area
    "schedule": ruleset_schedule.to_dict(), # ScheduleRuleset/ScheduleFixedInterval dictionary
    "radiant_fraction": 0.3, # fraction of heat that is long wave radiant
    "latent_fraction": 0, # fraction of heat that is latent
    "lost_fraction": 0 # fraction of heat that is lost
    }

    return ElectricEquipment.from_dict(elec_equip_dict)

def get_infiltration_gains(room):

    infiltration_dict = {
    "type": 'Infiltration',
    "identifier": f'Open_Office_Infiltration_{str(uuid.uuid4())[:8]}',
    "display_name": f'Office Infiltration {room.identifier}',
    "flow_per_exterior_area": 0.0003, # flow per square meter of exterior area
    "schedule": constant_on_ruleset_schedule.to_dict(), # ScheduleRuleset/ScheduleFixedInterval dictionary
    "constant_coefficient": 1, # optional constant coefficient
    "temperature_coefficient": 0, # optional temperature coefficient
    "velocity_coefficient": 0 # optional velocity coefficient
    }

    return Infiltration.from_dict(infiltration_dict)