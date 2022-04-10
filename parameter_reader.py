import re
import os
import json

file_name="CommonEvents.json"

json_file=open('CommonEvents.json')
json_data = json.load(json_file)
file_name_without_ext=file_name.split(".")[0]
f = open("{fn}.rpy".format(fn=file_name_without_ext),"w",encoding="utf-8")

#print (json_data[1]["list"][3])
#use id 256 for testing which has images
for per_list in json_data[256]["list"]:
    print (per_list)
    if per_list["parameters"]:
        print(len(per_list["parameters"]))
        #if (str(len(per_list["parameters"]) == "1")):
            #print (":::",per_list["parameters"][0])


        try:
            if ( per_list["parameters"][0] != ""  and not str(per_list["parameters"][0]).isdigit()):
                #print (per_list["parameters"][0])
                if (type(per_list["parameters"][0]) != list and str(per_list["parameters"][1]).isdigit()):
                    #print (":::",per_list["parameters"][0])
                    f.writelines("  "+per_list["parameters"][0])
                #if (type(per_list["parameters"][0]) != list and str(len(per_list["parameters"])) == "1"):
                if ( str(len(per_list["parameters"])) == "1"):
                    print ("Hello")
                    print (":::",per_list["parameters"][0])
                    f.writelines("  "+per_list["parameters"][0]+"\n")
        except:
            continue
        try:
            if ( per_list["parameters"][1] != "" and not str(per_list["parameters"][1]).isdigit()):
                #print ("scene ",per_list["parameters"][1])
                f.writelines("scene ",per_list["parameters"][1]+"\n")
        except:
            continue   
#number of ids approx 1090
'''
c=0
for i in json_data:
    c+=1
    print (json_data[c]["id"])
'''

'''
#list value of id 1
print (json_data[1]["list"])

for i in json_data[1]:
    print (i)
'''