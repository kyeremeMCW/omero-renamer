from omero.gateway import BlitzGateway, ImageWrapper
from collections import Counter
import re
conn = BlitzGateway('','', host= 'lavlab.mcw.edu', secure= True)
conn.connect()


#OmeRenamer
#Used to standardize names for images on Omero
#names should be N###_S##_Large_~stain~_?Deeper_#.ome.tiff - *Large for Brain 
#appened naming block with x.save() to commit changes
#start at the beggining of the name and move towards the end
#fix numbers before adding letters


#working on 0's, slide numbers, condensing if statements, semi standardize before dupe check 

patterns = ['SOX2', 'IDH1', 'KI67', 'Ki67', 'ERG', 'PTEN', 'CD31', 'STAT5', 'temp' , 'Deeper'] #dif naming blocks

for x in conn.getObjects('image'):
    if not any(pattern in x.getName() for pattern in patterns):
        print(x.getName())

#     if not '_T'in x.getName(): # ###_T# slides - ignoring for now

# adding 0's to make double digited slide number --- WIP
    if  re.match('.*_[0-9]_.*', x.getName()):
        print(x.getName())
        old_name = x.getName()
        new_name = re.sub(r'(_)([0-9])(_)', r'\g<1>0\2\3', old_name)
        x.setName(new_name)
        print('check 0')
        print(x.getName())

#adding N to patient number  ###_ is patient number -> N###_
    if re.match('^\d{3}_', x.getName()): 
        print(x.getName())
        old_name = x.getName()
        new_name = re.sub('^(\d{3}_)', r'N\1', old_name)
        x.setName(new_name)
        print('check N')
        print(x.getName())        

#adding S to slide number  _##_ is slide number -> _S##_ --- WIP
    if  re.match('.*_\d{2}_', x.getName()):
        print(x.getName())
        old_name = x.getName()
        new_name = re.sub(r'(_)(\d{2})', r'\1S\2', old_name)
        x.setName(new_name)
        print('check S')
        print(x.getName())  

#Large - brain exclusive. brains should have large in name, adding HE if missing 
    if  '_Large_' not in x.getName(): 
        print(x.getName())
        old_name = x.getName()
        new_name = old_name.replace('_Large', '_Large_HE')
        x.setName(new_name)
        print('check Large')
        print(x.getName())

#add HE if missing, need to change per instance --- WIP
    if not re.match('.*HE.*',  x.getName()) and not any(pattern in x.getName() for pattern in patterns):
        print(x.getName())
        old_name = x.getName()
        new_name = old_name.replace #what to replace with _HE ('', '_HE_temp')
        x.setName(new_name)
        print('check HE')
        print(x.getName())

#Deeper, similar to Large
    if '_Deeper' in x.getName() and not any(re.match(fr'.*{pattern}.*', x.getName()) for pattern in patterns): 
        print(x.getName())
        old_name = x.getName()
        new_name = old_name.replace('_Deeper', '_HE_Deeper')
        x.setName(new_name)
        print('check deeper')
        print(x.getName())

#remove Rescan
    if re.search(r'_Rescan\d{2}', x.getName()): 
        print(x.getName())
        old_name = x.getName()
        new_name = re.sub('_Rescan\d{2}', '', old_name)
        x.setName(new_name)
        print('check rescan')
        print(x.getName())