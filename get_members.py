import base64
import os
import requests

# 1. Safely pull credentials from GitHub Secrets
USERNAME = os.getenv("VRC_USERNAME")
PASSWORD = os.getenv("VRC_PASSWORD")
GROUP_ID = "grp_4afbd931-4ba6-4bcd-a5f7-5672e0671a9e"

if not USERNAME or not PASSWORD:
    print("Error: Missing VRChat credentials.")
    exit(1)

# VRChat API Base URL
BASE_URL = "https://api.vrchat.cloud/api/1"

# Manuelle Base64-Kodierung mit UTF-8 (behebt den Unicode-Fehler bei Sonderzeichen)
credentials = f"{USERNAME}:{PASSWORD}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

headers = {
    "User-Agent": "MyVRCWorldBot/1.0 (your-email@example.com)",
    "Authorization": f"Basic {encoded_credentials}"
}

# 2. Authenticate
auth_url = f"{BASE_URL}/auth/user"
response = requests.get(auth_url, headers=headers)

if response.status_code != 200:
    print(f"Authentication failed: {response.status_code} - {response.text}")
    exit(1)

# 3. Fetch all group members with pagination
members_url = f"{BASE_URL}/groups/{GROUP_ID}/members"
all_members = []
offset = 0

while True:
    params = {"offset": offset, "n": 100}
    res = requests.get(members_url, params=params, cookies=response.cookies, headers=headers)
    
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

# 4. Save to the file that will be pushed back to GitHub
output_text = ",".join(all_members)
with open("group_members.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Successfully generated member list with {len(all_members)} users.")
