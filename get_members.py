import os
import requests

# 1. Cookies aus den GitHub Secrets holen
AUTH_COOKIE = os.getenv("VRC_AUTH_COOKIE")
TWO_FACTOR_COOKIE = os.getenv("VRC_2FA_COOKIE")
GROUP_ID = "grp_4afbd931-4ba6-4bcd-a5f7-5672e0671a9e"

if not AUTH_COOKIE:
    print("Error: Missing VRC_AUTH_COOKIE secret.")
    exit(1)

# VRChat API Base URL und Headers
BASE_URL = "https://api.vrchat.cloud/api/1"
headers = {
    "User-Agent": "MyVRCWorldBot/1.0 (deine-echte-email@gmail.com)"
}

# Beide Cookies in das Dictionary packen
cookies = {
    "auth": AUTH_COOKIE
}
if TWO_FACTOR_COOKIE:
    cookies["twoFactorAuth"] = TWO_FACTOR_COOKIE

# 2. Authentifizierung prüfen
auth_url = f"{BASE_URL}/auth/user"
response = requests.get(auth_url, cookies=cookies, headers=headers)

if response.status_code != 200:
    print(f"Authentication failed: {response.status_code} - {response.text}")
    exit(1)

print("Successfully authenticated via Cookies!")

# 3. Gruppenmitglieder mit Pagination abrufen
members_url = f"{BASE_URL}/groups/{GROUP_ID}/members"
all_members = []
offset = 0

while True:
    params = {"offset": offset, "n": 100}
    res = requests.get(members_url, params=params, cookies=cookies, headers=headers)
    
    if res.status_code != 200:
        print(f"Failed to fetch members at offset {offset}: {res.status_code} - {res.text}")
        break
        
    data = res.json()
    
    if not data or len(data) == 0:
        break
        
    for member in data:
        if 'user' in member and 'displayName' in member['user']:
            all_members.append(member['user']['displayName'])
        elif 'displayName' in member:
            all_members.append(member['displayName'])
            
    offset += 100

# 4. In Datei speichern
output_text = ",".join(all_members)
with open("group_members.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Successfully generated member list with {len(all_members)} users.")
