import requests

# Home Assistant URL (change to your setup)
HOME_ASSISTANT_URL = "http://homeassistant.local:8123"

# Long-Lived Access Token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ.5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def change_temperature(entity_id, value=19):
    url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    data = {
        "entity_id": entity_id,
        "value": value
    }
    
    response = requests.post(url, json=data, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"{entity_id} turned on successfully!")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Example usage
#change_temperature("input_number.heating_temperature")#akl
