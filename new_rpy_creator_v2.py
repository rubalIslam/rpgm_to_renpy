import re
import os
import json

common_file_name="CommonEvents.json"
#movies_file_name="CommonEvents.json"

common_json_file=open(common_file_name)
movies_file_name = open("movies.rpy","w",encoding="utf-8")
common_json_data = json.load(common_json_file)
system_file = open("System.json")
system_file = json.load(system_file)


#print ("common_id::",common_json_data[664]["name"])

for x in range(8,9):
    file_name = "Map{}.json".format(f'{x:03}')
    #file_name = "Map096.json"
    #print (file_name)
    #file_name="Map019.json"
    #file_name="CommonEvents.json"

    json_file=open(file_name,encoding="utf8")
    json_data = json.load(json_file)
    file_name_without_ext=file_name.split(".")[0]
    
    count = 0
    current_char = ""
    prev_dialogue = ""
    sayer_list = []
    menu_name = []
    menu_name0 = ""
    menu_name1 = ""
    menu_name2 = ""
    menu_name3 = ""
    menu_name4 = ""
    menu_name5 = ""
    prev_dialogue = ""

    print (json_data["parallaxName"])

    #map_name = json_data["parallaxName"]

    num_pattern =  r'[^0-9]+'
    map_num = str(re.sub(num_pattern,'',file_name_without_ext))
    map_num = int(map_num.lstrip('0'))

    #print ("map_num::",map_num)


    map_file = open("Mapinfos.json")
    json_map = json.load(map_file)
    #print (json_map[map_num]["name"])
    map_name = json_map[map_num]["name"].replace(" ", "_")
    name_pattern =  r'[^A-Za-z0-9_]+'
    map_name = str(re.sub(name_pattern,'',map_name))
    print (map_name)

    f = open("{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")
    sayers = open("sayer.rpy","w",encoding="utf-8")

    ev = open("events_list_{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")

    count = 0
    for events in json_data["events"]:
        
        if json_data["events"][count] is not None:
            event_id = json_data["events"][count]["id"]
            event_name = json_data["events"][count]["name"]
            event_note = json_data["events"][count]["note"]
            label_name = str(map_name)+"_"+str(event_name)+str(event_note)+"_"+str(event_id)
            
            character_name = ""
            for pages in json_data["events"][count]["pages"]:
                switch_id = pages["conditions"]["switch1Id"]
                switch = system_file["switches"][switch_id]
                label = label_name+"_"+str(switch).replace(" ","_")
                pattern = r'[^A-Za-z0-9_ ]+'
                label = re.sub(pattern, '', label).lower()
                switch = re.sub(pattern, '',switch)
                switch = str(switch).replace(" ","_").lower()

                f.writelines('label {}:\n'.format(label.replace(" ","_")))
                ev.writelines('label {}:\n'.format(label.replace(" ","_")))
                
                f.writelines("    #switch: {} = True\n".format(switch))
                ev.writelines("    #switch: {} = True\n".format(switch))
                
                variable_id = pages["conditions"]["variableId"]
                variable_value = pages["conditions"]["variableValue"]
                variable = system_file["variables"][variable_id]
                variable = variable.replace(" ","_")
                variable = re.sub(pattern, '',variable).lower()
                f.writelines("    #variables: {} = {}\n".format(variable,variable_value))
                ev.writelines("    #variables: {} = {}\n".format(variable,variable_value))
               
                padding = 0
                for per_list in pages["list"]:
                    
                    code = str(per_list["code"])
                    if code == "111":
                        if per_list["parameters"][0] == 1:
                            params = ['==', '>=', '<=', '>', '<', '!=']
                            variable_name = system_file["variables"][per_list["parameters"][1]]
                            variable_params = int(per_list["parameters"][4])
                            
                            numerator = str(params[variable_params])
                            variable_comperator = str(per_list["parameters"][3])
                            #if padding == 0:
                            
                            variable_name = re.sub(pattern, '',variable_name).lower()
                            variable_name = variable_name.replace(" ","_")
                            f.writelines("  "*padding+"    if {} {} {}:\n".format(variable_name,numerator,variable_comperator))
                            padding += 2
                        elif per_list["parameters"][0] == 0:
                            on_off = ["on","off"]
                            on_off_value = int(per_list["parameters"][2])
                            #if padding == 0:
                            switch_name = system_file["switches"][int(per_list["parameters"][1])]
                            switch_name = re.sub(pattern,'',str(switch_name))
                            switch_name = switch_name.replace(" ","_").lower()
                            f.writelines('  '*padding+'    if switch_{} == "{}"\n'.format(switch_name,on_off[on_off_value]))
                            padding += 2
                    if code == "231":
                        scene_name = per_list["parameters"][1]
                        #if padding == 0:
                        f.writelines("  "*padding+"    scene {}\n".format(scene_name))
                        
                    if code == "101":
                        char_name = per_list["parameters"][0]
                        character_name = str(char_name).strip()
                        #f.writelines("\n  {} ".format(character_name))
                    if code == "401":
                        dialogue = per_list["parameters"][0]
                        if character_name == "":
                            #if padding == 0:
                            f.writelines('  '*padding+'    "{}"\n'.format(dialogue))
                            
                        else:
                            #if padding == 0:
                            f.writelines('  '*padding+'    {} "{}"\n'.format(character_name,dialogue))
                    if code == "122":
                        if per_list["parameters"][3] == 0:
                            set_variable_name = system_file["variables"][per_list["parameters"][1]]
                            set_variable_value = per_list["parameters"][4]
                            set_variable_name = re.sub(pattern,'',set_variable_name)
                            set_variable_name = set_variable_name.replace(" ","_").lower()
                            f.writelines("  "*padding+"    $ {} = {}\n".format(set_variable_name,set_variable_value))
                            
                    if code == "121":
                        on_off = ["True","False"]
                        set_switch_name = system_file["switches"][int(per_list["parameters"][1])]
                        true_false_value = on_off[per_list["parameters"][2]]
                        #if padding == 0:
                        set_switch_name = re.sub(pattern,'',str(set_switch_name).lower())
                        set_switch_name = set_switch_name.replace(" ","_")
                        f.writelines("  "*padding+"    $ switch_{} = {}\n".format(set_switch_name,true_false_value))
                        
                    if code == "201":
                        set_map_num = per_list["parameters"][1]
                        set_map_name = json_map[set_map_num]["name"]
                        #if padding == 0:
                        f.writelines("  "*padding+"    call {}\n".format(set_map_name))
                        
                    if code == "411":
                        #if padding == 0:
                        f.writelines("  "*padding+"    else:\n")
                        padding += 2
                        #else:
                        #    f.writelines("    {}".format(padding))
                    if code == "0":
                        padding -= 2
                    if code == "355":
                        variable_set = per_list["parameters"][0]
                        variable_type = variable_set.split(".")
                        if variable_type[0] == "$gameVariables":
                            if "(" in str(variable_set):
                                variable_name = variable_set.split("(")
                                variable_number = variable_name[1].split(",")[0]
                                variable = system_file["variables"][int(variable_number)]
                                if '"' in variable_set:
                                    variable_value = variable_set.split('"')
                                    variable = re.sub(pattern, '',str(variable))
                                    variable = variable.replace(" ","_")
                                    f.writelines('  '*padding+'    $ {} = "{}"\n'.format(variable,variable_value[1]))
                        elif variable_type[0] == "ysp":
                            if "(" in str(variable_set):
                                if "newVideo" in str(variable_set):
                                    video_name = variable_set.split("'")[1]
                                    f.writelines("  "*padding+"    #play video {}\n".format(video_name))

        count+=1    

        #for json_list in json_data["events"][count]["pages"]:
        #    print(json_list["conditions"])
