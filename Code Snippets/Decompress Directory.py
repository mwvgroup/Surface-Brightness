#!/usr/bin/env python3
import zipfile, os, gzip
directory = "."
    
for path, subdirs, files in os.walk(directory):
    for name in files:
        if ".gz" in name:

            inF = gzip.open(os.path.join(path, name), 'rb')
            data = inF.read()
            inF.close()

            outF = open(os.path.join(path, name).replace('.gz',''), 'wb')
            outF.write(data)
            outF.close()
            
            os.remove(os.path.join(path, name))
            
        elif ".zip" in name:
            zip_ref = zipfile.ZipFile(os.path.join(path, name), 'r')
            zip_ref.extractall(path)
            zip_ref.close()
            
            os.remove(os.path.join(path, name))