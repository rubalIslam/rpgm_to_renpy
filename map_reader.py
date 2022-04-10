import re
import os
import json

for x in range(1,131):
    #print("Map{}.json".format(f'{x:03}'))
    file_name = "Map{}.json".format(f'{x:03}')

    #file_name="Map013.json"

    json_file=open(file_name)
    json_data = json.load(json_file)
    file_name_without_ext=file_name.split(".")[0]
    f = open("{fn}.rpy".format(fn=file_name_without_ext),"w",encoding="utf-8")
    sayers = open("sayer.rpy","w",encoding="utf-8")
    count = 0
    current_char = ""
    prev_dialogue = ""
    sayer_list = []

    print (json_data["parallaxName"])

    #map_name = json_data["parallaxName"]

    num_pattern =  r'[^1-9]+'
    map_num = int(re.sub(num_pattern,'',file_name_without_ext))

    #print (map_num)


    map_file = open("Mapinfos.json")
    json_map = json.load(map_file)
    #print (json_map[map_num]["name"])
    map_name = json_map[map_num]["name"].replace(" ", "_")
    print (map_name)

    count = 0
    for i in json_data["events"]:
        count+=1
        #print (json_data["events"][count]["pages"])
        try:
            for json_list in json_data["events"][count]["pages"]:
                #print (json_list["list"])
                #print (json_list["list"][2]["parameters"])
                label_with_underscore = json_data["events"][count]["name"].replace(" ","")
                note_with_underscore = json_data["events"][count]["note"].replace(" ","_")
                if (label_with_underscore == "Timeofday"):
                    first_label = str(file_name_without_ext)
                    print(first_label)
                    f.writelines('\nlabel {}:\n'.format(first_label))
                else:
                    pattern = r'[^A-Za-z0-9_]+'
                    label_without_special_char = re.sub(pattern, '', label_with_underscore)
                    mote_without_special_char = re.sub(pattern, '', note_with_underscore)
                    f.writelines('\nlabel {}:\n'.format(label_without_special_char+mote_without_special_char+"_"+map_name))
                for per_list in json_list["list"]:
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
                                        #print(current_char_split[0])
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
                        #if "GwynnethandInnkeeper" in per_list["parameters"][0]: 
                        #    print(per_list["parameters"])
                        if ( per_list["parameters"][1] != "" and not str(per_list["parameters"][1]).isdigit()):
                            lower_of_scene = per_list["parameters"][1].lower()
                            if "missing" not in lower_of_scene:
                                f.writelines("  scene {} \n".format(lower_of_scene))
        except:
            print("exception")    
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
    

    #use id 256 for testing which has images
    count = 0
    current_char = ""
    prev_dialogue = ""
    sayer_list = []
    