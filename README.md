# get_cloudflare_registers
Python script to retrieve all A and CNAME registers  from a cloudflare domain

Usage: 

python3 get_cloudflare_registers.py <Bearer key> [--output-file file.<html/htm/xls>] [--debug <level>] [--exceptions file.txt]



#
# Generating Cloudlfare API authentication Bearer key process:
#
# Once logged on https://dash.cloudflare.com goto

# My profile > API Tokens > Create Tokens > Read all resources > Use Template > Set up a name for API key, example "Scripts_RO"
# You can use readonly template and modify to remove unused permissions and  > Continue to summary
# Bearer key is provided only one time

Parameters: 

 zone_key: Mandatory - Specifies your Cloudflare API key with premissions to read information from your account. 
 debug: Optional - Specifies debug level 0,1 or 2 
 output_file: Specifies ouput file name/path, it can create and XLS or HTML file depending on file extension you specify 
 exceptions: Specifies a txt which contains records to be ignored if proxy is disabled. 

Example: 

python3 get_cloudflare_registers.py 4jO0k3G-T0fMLl60aBVZnUT2ad33a --debug 2 --output-file output_file.xls --exceptions exceptions.txt

Another example: 

Given a tokens_zonas.csv file with this format

zone1,token1
zone2,token2
zone3,token3 
... 

awk -F, '{print $2}' tokens_zones.csv | xargs -i python3 get_cloudflare_registers.py {} 1
