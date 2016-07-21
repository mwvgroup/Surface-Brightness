#!/usr/bin/env python3
import os, gzip, shutil
in_directory = "/Volumes/Media RED/fits files/Rigault 15 Supernova/"
out_directory =  in_directory.rstrip('/') + ' comp/'

n = 0

if os.path.exists(in_directory):
    for path, subdirs, files in os.walk(in_directory):
        for name in files:
            if ".fits" in name:
                
                in_path = os.path.join(path, name)
                out_dir = path.replace(in_directory, out_directory)
                out_path = os.path.join(out_dir, name + '.gz')
                
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
        
                print(in_path, flush = True)
                with open(in_path, 'rb') as f_in, gzip.open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                
                n += 1
                
    print('\nFinished:', n, 'files compressed')
    
else:
    print("Input directory does not exist")
