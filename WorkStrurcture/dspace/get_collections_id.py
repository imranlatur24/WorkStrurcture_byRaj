#1.we are scrapping dspace exported data here by using exported csv file
#2.each 24 hrs file is scrapped here by using same script
#3.increase max size for export csv file follow below link
#http://dspace.2283337.n4.nabble.com/DSpace-collection-export-maximum-size-td4661822.html
import os
os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f C:\Users\3029\Documents\export\colllectionitem.csv -i 123456789/"')
