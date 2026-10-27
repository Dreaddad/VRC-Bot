import os
import requests

# 1. Safely pull credentials from GitHub Secrets
USERNAME = os.getenv("VRC_USERNAME")
PASSWORD = os.getenv("VRC_PASSWORD")
GROUP_ID = "https://vrchat.com/home/group/grp_4afbd931-4ba6-4bcd-a5f7-5672e0671a9e" # Paste your actual group ID here

if not USERNAME or not PASSWORD:
    print("Error: Missing VRChat credentials.")
    exit(1)

# 2. Authenticate
auth_url = "https://vrchat.cloud"
headers = {"User-Agent": "MyVRCWorldBot/1.0"}
response = requests.get(auth_url, auth=(USERNAME, PASSWORD), headers=headers)

# 3. Fetch all group members
members_url = f"https://vrchat.cloud{GROUP_ID}/members"
all_members = []
n = 0

while True:
    params = {"offset": n, "n": 100}
    res = requests.get(members_url, params=params, cookies=response.cookies, headers=headers)
    data = res.json()
    
    if not data or len(data) == 0:
        break
        
    for member in data:
        all_members.append(member['user']['displayName'])
        
    n += 100

# 4. Save to the file that will be pushed back to GitHub
output_text = ",".join(all_members)
with open("group_members.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"Successfully generated member list with {len(all_members)} users.")
