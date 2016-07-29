#!/usr/bin/env python3
import requests
import urllib
import json
from astropy.table import Table

sn_list_file = 'observed targets data table.csv'
sn_col = 0

#Github directories from the open supernova catalougue
sne_1990_to_1999 = 'https://raw.githubusercontent.com/astrocatalogs/sne-1990-1999/master/'
sne_2000_to_2004 = 'https://raw.githubusercontent.com/astrocatalogs/sne-2000-2004/master/'
sne_2005_to_2009 = 'https://raw.githubusercontent.com/astrocatalogs/sne-2005-2009/master/'
sne_2010_to_2014 = 'https://raw.githubusercontent.com/astrocatalogs/sne-2010-2014/master/'
sne_2015_to_2019 = 'https://raw.githubusercontent.com/astrocatalogs/sne-2015-2019/master/'
dir_list = [sne_1990_to_1999, sne_2000_to_2004, sne_2005_to_2009, sne_2010_to_2014, sne_2015_to_2019]

#Create the input table of sn and an empty output table
    #Note that the case of the supernova names in your input files matters
sn_table = Table.read(sn_list_file, format='ascii.csv')
data_table = Table(names = ['sn', 'z', 'RA', 'Dec'],
                   dtype = [object, object, object, object])

for row in sn_table:
    found = False
    
    #First we try quicker method and assume the sn name is of the form sn####abc
    try:
        if 1990 <= int(row[sn_col][2:6]) <= 1999:
            r = requests.get(sne_1990_to_1999 + urllib.parse.quote(row[sn_col]) + '.json')
            data = json.loads(r.text)
            
            z = data[row[sn_col]]['redshift'][0]['value']
            
            if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                ra = data[row[sn_col]]['ra'][0]['value']
                dec = data[row[sn_col]]['dec'][0]['value']
            
            else:
                ra = 'N/A'
                dec = 'N/A'
            
            data_table.add_row([row[sn_col], z, ra, dec])
            found = True
            
        elif 2000 <= int(row[sn_col][2:6]) <= 2004:
            r = requests.get(sne_1990_to_1999 + urllib.parse.quote(row[sn_col]) + '.json')
            data = json.loads(r.text)
            
            z = data[row[sn_col]]['redshift'][0]['value']
            
            if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                ra = data[row[sn_col]]['ra'][0]['value']
                dec = data[row[sn_col]]['dec'][0]['value']
            
            else:
                ra = 'N/A'
                dec = 'N/A'
            
            data_table.add_row([row[sn_col], z, ra, dec])
            found = True
            
        elif 2005 <= int(row[sn_col][2:6]) <= 2009:
            r = requests.get(sne_1990_to_1999 + urllib.parse.quote(row[sn_col]) + '.json')
            data = json.loads(r.text)
            
            z = data[row[sn_col]]['redshift'][0]['value']
            
            if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                ra = data[row[sn_col]]['ra'][0]['value']
                dec = data[row[sn_col]]['dec'][0]['value']
            
            else:
                ra = 'N/A'
                dec = 'N/A'
            
            data_table.add_row([row[sn_col], z, ra, dec])
            found = True
            
        elif 2010 <= int(row[sn_col][2:6]) <= 2014:
            r = requests.get(sne_1990_to_1999 + urllib.parse.quote(row[sn_col]) + '.json')
            data = json.loads(r.text)
            
            z = data[row[sn_col]]['redshift'][0]['value']
            
            if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                ra = data[row[sn_col]]['ra'][0]['value']
                dec = data[row[sn_col]]['dec'][0]['value']
            
            else:
                ra = 'N/A'
                dec = 'N/A'
            
            data_table.add_row([row[sn_col], z, ra, dec])
            found = True
        
        elif 2015 <= int(row[sn_col][2:6]) <= 2019:
            r = requests.get(sne_1990_to_1999 + urllib.parse.quote(row[sn_col]) + '.json')
            data = json.loads(r.text)
            
            z = data[row[sn_col]]['redshift'][0]['value']
            
            if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                ra = data[row[sn_col]]['ra'][0]['value']
                dec = data[row[sn_col]]['dec'][0]['value']
            
            else:
                ra = 'N/A'
                dec = 'N/A'
            
            data_table.add_row([row[sn_col], z, ra, dec])
            found = True
    
    except ValueError:
        pass
    
    except Exception as e:
        print('Exception for', row[sn_col])
        print(e, '\n', flush = True)
    
    #If the method above didn't work - we loop through all possibilities
    if found == False:
        for github_dir in dir_list:
            r = requests.get(github_dir + urllib.parse.quote(row[sn_col]) + '.json')
            if '404: Not Found' not in r.text:
                data = json.loads(r.text)
                
                z = data[row[sn_col]]['redshift'][0]['value']
                
                if 'ra' in data[row[sn_col]] and 'dec' in data[row[sn_col]]:
                    ra = data[row[sn_col]]['ra'][0]['value']
                    dec = data[row[sn_col]]['dec'][0]['value']
                
                else:
                    ra = 'N/A'
                    dec = 'N/A'
                
                data_table.add_row([row[sn_col], z, ra, dec])
                found = True
                break
    
    if found == False:
        print('Could not find', row[sn_col], flush = True)

data_table.write('OSE Data Table.csv', format = 'ascii.csv')
