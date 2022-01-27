#1.we are scrapping dspace exported data here by using exported csv file
#2.each 24 hrs file is scrapped here by using same script
#3.increase max size for export csv file follow below link
#http://dspace.2283337.n4.nabble.com/DSpace-collection-export-maximum-size-td4661822.html
import os
                                                                                                                                                 
def export_community():
    arr = ['3','30','1','34','32'] # this data from Community
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace_15_nove_troubleshooting\Community\"'+i+".csv -i 108/"+i)
        print('done')

def export_community_23():
    arr = ['23'] # this data from Community
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace_15_nove_troubleshooting\23\"'+i+".csv -i 108/"+i)
        print('done')

# def export_community_32():
#     arr = ['32'] # this data from Community
#     for i in arr:
#         print(i)
#         os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace_15_nove_troubleshooting\32\"'+i+".csv -i 108/"+i)
#         print('done')

def export_collection():
    arr = ['14','16','19','20','22','17','18','21','45'] # this data from Community '14','16','19','20','22'
    for i in arr:
        print(i)
        os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace_15_nove_troubleshooting\Collection\"'+i+".csv -i 108/"+i)
        print('done')

# def export_collections_17_18_21_45():
#     arr = ['17','18','21','45'] # this data from Community '17','18','21','45'
#     for i in arr:
#         print(i)
#         os.system(r'cmd /c "C:\dspace\bin\dspace metadata-export -f E:\WorkStrurcture_byRaj\WorkStrurcture\dspace_15_nove_troubleshooting\collections_old\"'+i+".csv -i 108/"+i)
#         print('done')

export_community() #exporting data from commnity 1,3,4,5,6,7
export_community_23()
# export_community_32()
export_collection() #collection is only for standards commnity it is huge data
# export_collections_17_18_21_45()
