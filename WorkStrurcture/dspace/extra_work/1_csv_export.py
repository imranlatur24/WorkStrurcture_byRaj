#1.we are scrapping dspace exported data here by using exported csv file
#2.each 24 hrs file is scrapped here by using same script
#3.increase max size for export csv file follow below link
#http://dspace.2283337.n4.nabble.com/DSpace-collection-export-maximum-size-td4661822.html
import os
                                                                                                                                                 
#arr = [] this data for standard's collection
arr = ['3','23','30','32','1','34','14','45','16','17','18','19','20','21','22'] # this data from Community
for i in arr:
    print(i)
    #for Community export os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f C:\Users\3029\Documents\export\"'+i+".csv -i 123456789/"+i)
    os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f C:\Users\Administrator\Desktop\DSPACE_EXPORT\"'+i+".csv -i 108/"+i)
    print('done')