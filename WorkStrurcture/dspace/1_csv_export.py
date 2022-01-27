#1.we are scrapping dspace exported data here by using exported csv file
#2.each 24 hrs file is scrapped here by using same script
#3.increase max size for export csv file follow below link
#http://dspace.2283337.n4.nabble.com/DSpace-collection-export-maximum-size-td4661822.html
import os
                                                                                                                                                 
def export_community():
    arr = ['3','13','23','30','32','1','34'] # this data from Community
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace\Community\"'+i+".csv -i 108/"+i)
        print('done')


def export_collection():
    arr = ['14','45','16','17','18','19','20','21','22'] # this data from Community
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace\Collection\"'+i+".csv -i 108/"+i)
        print('done')

export_community() #exporting data from commnity 1,3,4,5,6,7
export_collection() #collection is only for standards commnity it is huge data

