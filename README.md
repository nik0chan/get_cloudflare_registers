# get_cloudflare_registers
Python script to retrieve all A and CNAME registers  from a cloudflare domain

Usage: 

 python3 /root/scripts/cloudflare/get_cloudflare_registers.py <zone_key> [debug level] [output_file]

Parameters: 

 zone_key: Mandatory - Specifies your Cloudflare API key with premissions to read information from your account. 
 debug: Optional - Specifies debug level 0,1 or 2 
 output_file: Specifies ouput file name/path, it can create and XLS or HTML file depending on file extension you specify 

Example 
 
  python3 /root/scripts/cloudflare/get_cloudflare_registers.py wcFE2f4.2fñ429ef8cl32fj34klw99ñw 2 /tmp/output.html 

Another example: 

Given a tokens_zonas.csv file with this format

zone1,token1
zone2,token2
zone3,token3 
... 

awk -F, '{print $2}' tokens_zones.csv | xargs -i python3 get_cloudflare_registers.py {} 1
