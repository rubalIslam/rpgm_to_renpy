import re
import os
import json

file_name="Map002.json"

json_file=open(file_name)
json_data = json.load(json_file)
file_name_without_ext=file_name.split(".")[0]
f = open("{fn}.rpy".format(fn=file_name_without_ext),"w",encoding="utf-8")
sayers = open("sayer.rpy","w",encoding="utf-8")


#print (json_data[1]["list"][3])
#use id 256 for testing which has images
count = 0
current_char = ""
prev_dialogue = ""
sayer_list = []

for i in json_data:
    count+=1
    #print (json_data[count]["name"])
    try:
        if (json_data[count]["name"] != ""):
            label_with_underscore = json_data[count]["name"].replace(" ","")
            if (label_with_underscore == "Timeofday"):
                first_label = str(file_name_without_ext)
                print(first_label)
                f.writelines('\nlabel {}:\n'.format(first_label))
            else:
                pattern = r'[^A-Za-z0-9_]+'
                label_without_special_char = re.sub(pattern, '', label_with_underscore)
                f.writelines('\nlabel {}:\n'.format(label_without_special_char))
            for per_list in json_data[count]["list"]:
                #print (per_list)
                if per_list["parameters"]:
                    #print(len(per_list["parameters"]))
                    #if (str(len(per_list["parameters"]) == "1")):
                    #print (":::",per_list["parameters"][0])
                    if (str(len(per_list["parameters"])) == "1" or str(len(per_list["parameters"])) == "4"):
                        if (str(len(per_list["parameters"])) == "4" and not str(per_list["parameters"][0]).isdigit()):
                            #print (":::",per_list["parameters"][0])
                            current_char = per_list["parameters"][0]

                            if current_char not in sayer_list:
                                sayer_list.append(current_char)
                        if (str(len(per_list["parameters"])) == "1" and not str(per_list["parameters"][0]).isdigit() and per_list["parameters"][0] != ""):
                            #print (":::",per_list["parameters"][0])
                            if (prev_dialogue != per_list["parameters"][0] and "{" not in str(per_list["parameters"][0])):
                                if (current_char.strip() == ""):
                                    dialogue_without_quotes=str(per_list["parameters"][0]).replace('"',"'")
                                    pattern = r'[^A-Za-z0-9_ ]+'
                                    dialogue_without_special_char = re.sub(pattern, '', dialogue_without_quotes)
                                    f.writelines('  \"{}\"\n'.format(dialogue_without_special_char))
                                    prev_dialogue = per_list["parameters"][0]
                                    continue
                                if (current_char.strip() != "" and "{" not in str(per_list["parameters"][0])):
                                    dialogue_without_quotes=str(per_list["parameters"][0]).replace('"',"'")
                                    pattern = r'[^A-Za-z0-9_ ]+'
                                    dialogue_without_special_char = re.sub(pattern, '', dialogue_without_quotes)
                                    if "-" in current_char:
                                        current_char_split = current_char.split("-")
                                        f.writelines('  {}  \"{}\"\n'.format(current_char_split[0],dialogue_without_special_char))
                                        prev_dialogue = per_list["parameters"][0]
                                        continue
                                    if " " in current_char:
                                        current_char_split = current_char.split(" ")
                                        f.writelines('  {}  \"{}\"\n'.format(current_char_split[0],dialogue_without_special_char))
                                        prev_dialogue = per_list["parameters"][0]
                                        continue
                                    if "-" not in current_char and " " not in current_char:    
                                        f.writelines('  {}  \"{}\"\n'.format(current_char,dialogue_without_special_char))
                                        prev_dialogue = per_list["parameters"][0]
                                        continue
                            continue
                    if (str(len(per_list["parameters"])) == "10"):
                        if ( per_list["parameters"][1] != "" and not str(per_list["parameters"][1]).isdigit()):
                            lower_of_scene = per_list["parameters"][1].lower()
                            if "missing" not in lower_of_scene:
                                f.writelines("  scene {} \n".format(lower_of_scene))
    except:
        print ("ignoring")
#print (sayer_list)
for sayer in sayer_list:
    if (sayer.strip() != ""):
        if "-" in sayer:
            sayer_name_split = sayer.split("-")
            sayers.writelines("define {} = Character ('{}', color=\"#AAAAAA\", who_outlines=[ (2, \"#000000\") ], what_outlines=[ (2, \"#000000\") ])\n".format(sayer_name_split[0],sayer_name_split[0]))
            continue        
        if " " in sayer:
            sayer_name_split = sayer.split(" ")
            sayers.writelines("define {} = Character ('{}', color=\"#AAAAAA\", who_outlines=[ (2, \"#000000\") ], what_outlines=[ (2, \"#000000\") ])\n".format(sayer_name_split[0],sayer_name_split[0]))
            continue        
        else:
            sayers.writelines("define {} = Character ('{}', color=\"#AAAAAA\", who_outlines=[ (2, \"#000000\") ], what_outlines=[ (2, \"#000000\") ])\n".format(sayer,sayer))
       

#number of ids approx 1090
'''
c=0
for i in json_data:
    c+=1
    print (json_data[c]["id"])
    print (json_data[c]["name"])

'''
'''
#list value of id 1
print (json_data[1]["list"])

for i in json_data[1]:
    print (i)
'''