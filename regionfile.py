# Region Selection File

def regionselector(region):

    if region == "atl":
        lat_min = 0
        lat_max = 60
        lon_min = -100
        lon_max = -5
        region = "Atlantic"
        dataset = "hurdat_atl"

    elif region == "watl":
        lat_min = 5
        lat_max = 40
        lon_min = -105
        lon_max = -50
        region = "West Atlantic"
        dataset = "hurdat_atl"

    elif region == "gom":
        lat_min = 15
        lat_max = 35
        lon_min = -105
        lon_max = -75
        region = "Gulf of Mexico"
        dataset = "hurdat_atl"

    elif region == "nwatl":
        lat_min = 20
        lat_max = 50
        lon_min = -90
        lon_max = -50
        region = "Northwest Atlantic"
        dataset = "hurdat_atl"

    elif region == "subtropicalatl":
        lat_min = 20
        lat_max = 50
        lon_min = -85
        lon_max = -5
        region = "Subtropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "ncatl":
        lat_min = 20
        lat_max = 50
        lon_min = -70
        lon_max = -30
        region = "North-Central Atlantic"
        dataset = "hurdat_atl"

    elif region == "neatl":
        lat_min = 20
        lat_max = 50
        lon_min = -40
        lon_max = -5
        region = "Northeast Atlantic"
        dataset = "hurdat_atl"

    elif region == "carib":
        lat_min = 5
        lat_max = 25
        lon_min = -90
        lon_max = -60
        region = "Caribbean"
        dataset = "hurdat_atl"

    elif region == "opentropatl":
        lat_min = 5
        lat_max = 25
        lon_min = -65
        lon_max = -15
        region = "Tropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "etropatl":
        lat_min = 5
        lat_max = 25
        lon_min = -40
        lon_max = -15
        region = "Eastern Tropical Atlantic"
        dataset = "hurdat_atl"

    elif region == "aew":
        lat_min = 0
        lat_max = 25
        lon_min = -40
        lon_max = 40
        region = "Eastern Tropical Atlantic, Sahel and Southern Sahara"
        dataset = "hurdat_atl"

    elif region == "wpac":
        lat_min = 0
        lat_max = 50
        lon_min = 100
        lon_max = 180
        region = "Western Pacific"
        dataset = "jtwc_wp"

    elif region == "ph":
        lat_min = 0
        lat_max = 25
        lon_min = 120
        lon_max = 145
        region = "Philippine Sea"
        dataset = "jtwc_wp"

    elif region == "med":
        lat_min = 30
        lat_max = 50
        lon_min = -10
        lon_max = 45
        region = "Mediterranean"
        dataset = None

    elif region == "cmed":
        lat_min = 30
        lat_max = 42
        lon_min = 10
        lon_max = 25
        region = "Central Mediterranean"
        dataset = None

    elif region == "emed":
        lat_min = 30
        lat_max = 42
        lon_min = 20
        lon_max = 40
        region = "Eastern Mediterranean"
        dataset = None

    elif region == "global":
        lat_min = -60
        lat_max = 60
        lon_min = -180
        lon_max = 180
        region = "Global"
        dataset = "all"

    elif region == "southwest_indian":
        lat_min = -40
        lat_max = 0
        lon_min = 20
        lon_max = 90
        region = "South-West Indian Ocean"
        dataset = "jtwc_sh"

    return lat_min, lat_max, lon_min, lon_max, region, dataset