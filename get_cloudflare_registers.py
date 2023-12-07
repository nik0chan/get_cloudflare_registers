# get_cloudflare_registers.py
# NMS - 07/12/2023
# Description:
# Given an Cloudflare token identification bearer returns info for A/CNAME registers, proxy status and type of register of all domains configured for this zone
#
# Requirements:
#
# python3 -m pip install openpyxl
#
# Syntax: (Parameter Bearer key is mandatory):
# python3 get_cloudflare_registers.py <Bearer key> [--output-file file.<html/htm/xls>] [--debug <level>] [--exceptions file.txxt]
#
# Example: python3 get_cloudflare_registers.py 4jO0k3G-T0fMLl60aBVZnUT2ad33a --debug 2 --output-file output_file.xls --exceptions exceptions.txt
#
# Generating Cloudlfare API authentication Bearer key process:
#
# Once logged on https://dash.cloudflare.com goto
# My profile > API Tokens > Create Tokens > Read all resources > Use Template > Set up a name for API key, example "Scripts_RO"
# You can use readonly template and modify to remove unused permissions and  > Continue to summary
# Bearer key is provided only one time
import argparse
import requests
import json
import sys
import openpyxl

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

def write_to_html(records, output_file, exceptions, debug):
    with open(output_file, 'w') as f:
        if debug>1:
           print("Writting output to html file: ",output_file)
           print("Exceptions loaded: ",exceptions)
        f.write('<html><head>\n')
        f.write('<title>DNS Records</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
        f.write('</head><body>\n')
        f.write('<table class="styled-table">\n')
        f.write('<tr><th>Type</th><th>Name</th><th>Content</th><th>Proxy Enabled</th></tr>\n')
        for record in records:
            proxy_enabled = record["proxied"]

            if debug>2:
               print("Testing ",record["name"])
            if record["name"] in exceptions:
                if debug>2:
                    print("Exception found on for record: ",record["name"])
                f.write(f'<tr class="gray-row"><td>{record["type"]}</td><td>{record["name"]}</td><td>{record["content"]}</td><td>{record["proxied"]}</td></tr>\n')
            else:
               if proxy_enabled == 0:
                  f.write(f'<tr class="red-row"><td>{record["type"]}</td><td>{record["name"]}</td><td>{record["content"]}</td><td>{record["proxied"]}</td></tr>\n')
               else:
                  f.write(f'<tr><td>{record["type"]}</td><td>{record["name"]}</td><td>{record["content"]}</td><td>{record["proxied"]}</td></tr>\n')
        f.write('</table>\n')
        f.write('</body></html>\n')

def write_to_excel(records, output_file):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'DNS Records'

    ws.append(['Type', 'Name', 'Content', 'Proxy Enabled'])

    for record in records:
        ws.append([record["type"], record["name"], record["content"], record["proxied"]])

    wb.save(output_file)

def main(debug, output_file, exceptions):

   if debug:
        print("{:10}{:50}{:120}{:10}".format("Type", "Name", "Content", "Proxy_Enabled"))

   tokens = sys.argv[1]
   all_records = []

   if ',' in tokens: # Multiple CSV zone tokens
     for token in tokens.split(','):
         for zone in get_zone_identifiers(token, debug):
             for record in (get_dns_records(zone,"A",token,debug)):
                 if "domainkey" not in record['content']:
                    print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
                    all_records.append(record)
             for record in (get_dns_records(zone,"CNAME",token, debug)):
                 if "domainkey" not in record['content']:
                    print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
                    all_records.append(record)
   else: # Single token
     for zone in get_zone_identifiers(tokens, debug):
        for record in (get_dns_records(zone,"A",tokens,debug)):
            if "domainkey" not in record['content']:
               if debug >= 1:
                  print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
               all_records.append(record)
        for record in (get_dns_records(zone,"CNAME",tokens, debug)):
            if "domainkey" not in record['content']:
               if debug >= 1:
                  print(f"{record['type']:10}{record['name']:50}{record['content']:120}{record['proxied']:10}")
               all_records.append(record)

   if all_records and output_file != 'none': # File output
      if output_file.lower().endswith('.xls') or output_file.lower().endswith('.xlsx'):
         write_to_excel(all_records, output_file)
      elif output_file.lower().endswith('.htm') or output_file.lower().endswith('.html'):
          write_to_html(all_records, output_file, exceptions, debug)
      else:
         print("Format not supported on filename. Please use .xls, .xlsx or .htm .html format for output.")
         print("Example: ")
         print("python3 get_cloudflare_registers.py 4jO0k3G-T0fMLl60aBVZnUT2ad33a [debug] [output_file.xls] ")

if __name__ == '__main__':
   try:
       parser = argparse.ArgumentParser(description='Cloudflare DNS Records Script')
       parser.add_argument('token', help='Bearer token for Cloudflare API')
       parser.add_argument('--debug', type=int, default=1, help='Debug level (0, 1, or 2)')
       parser.add_argument('--output-file', default='none', help='Output file name (.xls, .xlsx, .htm, .html)')
       parser.add_argument('--exceptions', help='File containing DNS records to exclude')

       args = parser.parse_args()

       if args.exceptions:
           with open(args.exceptions, 'r') as exceptions_file:
               exceptions = [line.strip() for line in exceptions_file]
       else:
           exceptions = []

   except ValueError:
       print("ERROR - Unexpected input")
       print("Syntax: ")
       print("python3 get_cloudflare_registers.py 4jO0k3G-T0fMLl60aBVZnUT2ad33a --debug 2 --output-file output_file.xls --exceptions exceptions.txt")
       exit()


   main(args.debug, args.output_file, exceptions)
