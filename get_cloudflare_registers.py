# get_cloudflare_registers.py
# NMS - 26/08/2023
# Description:
# Given an Cloudflare token identification bearer returns info for A/CNAME registers, proxy status and type of register of all domains configured for this zone
# Syntax: (Parameter Bearer key is mandatory):
# python3 get_cloudflare_registers.py <Bearer key> [debug level] 
#
# Generating Cloudlfare API authentication Bearer key process:
#
# Once logged on https://dash.cloudflare.com goto
# My profile > API Tokens > Create Tokens > Read all resources > Use Template > Set up a name for API key, example "Scripts_RO"
# You can use readonly template and modify to remove unused permissions and  > Continue to summary
# Bearer key is provided only one time

import requests
import json
import sys

def get_dns_records(zone_id, record_type, key, debug=0):
    # Returns all registers on a zone, you must specify zone_id, record type "A/CNAME" and authentication Bearer
    # Limited to 100 registers by default you an increase specifying register_number paramether
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json"
    }

    params = {
        "type": record_type,
        "page": 1,
        "per_page": 100
    }

    if debug>1:
        print(f"Making request to {base_url} with params {params}")

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])
    else:
        print("Error:", response.text)
        return []

def get_zone_identifiers(bearer_token, debug=0):
    # Given an Bearer token returns all zone identifiers on a Cloudflare account
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    if debug>1:
        print("Making request to https://api.cloudflare.com/client/v4/zones/?per_page=400")

    response = requests.get('https://api.cloudflare.com/client/v4/zones/?per_page=400', headers=headers)
    data = json.loads(response.text)
    zone_ids = [zone['id'] for zone in data['result']]
    return zone_ids

def main(debug=0):
   if debug:
        print("{:10}{:50}{:120}{:10}".format("Type", "Name", "Content", "Proxy_Enabled"))
   for zone in get_zone_identifiers(sys.argv[1], debug):
      for record in (get_dns_records(zone,"CNAME",sys.argv[1],debug)):
            #print(record["type"],record["name"],record["content"],record["proxied"])
          print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
      for record in (get_dns_records(zone,"A",sys.argv[1], debug)):
          #  print(record["type"],record["name"],record["content"],record["proxied"])
          print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
if __name__ == '__main__':
    try:
       debug = int(sys.argv[2])
    except IndexError:
       debug = 0
    main(debug)
