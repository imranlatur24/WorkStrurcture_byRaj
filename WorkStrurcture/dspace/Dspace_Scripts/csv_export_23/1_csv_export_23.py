#1.we are scrapping dspace exported data here by using exported csv file
#2.each 24 hrs file is scrapped here by using same script
#3.increase max size for export csv file follow below link
#http://dspace.2283337.n4.nabble.com/DSpace-collection-export-maximum-size-td4661822.html
import os
                                                                                                                                                 
def export_community():
    arr = ['23'] # this data from Community
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace\23\"'+i+".csv -i 108/"+i)
        print('done')


export_community() #exporting data from commnity 1,3,4,5,6,7
#collection is only for standards commnity it is huge data

