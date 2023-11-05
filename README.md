# get_cloudflare_registers
Python script to retrieve all A and CNAME registers  from a cloudflare domain

Usage: 

 python3 /root/scripts/cloudflare/get_cloudflare_registers.py <zone_key> [debug level]

Parameters: 

 zone_key: Mandatory - Specifies your Cloudflare API key with premissions to read information from your account. 
 debug: Optional - Specifies debug level 0,1 or 2 

Example 
 
  python3 /root/scripts/cloudflare/get_cloudflare_registers.py wcFE2f4.2fñ429ef8cl32fj34klw99ñw 2

Another example: 

Given a tokens_zonas.csv file with this format

zone1,token1
zone2,token2
zone3,token3 
... 

awk -F, '{print $2}' tokens_zonas.csv | xargs -i python3 get_cloudflare_registers.py {} 0
