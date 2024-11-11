import re
import os
import json

common_file_name="CommonEvents.json"
#movies_file_name="CommonEvents.json"

common_json_file=open(common_file_name)
movies_file_name = open("movies.rpy","w",encoding="utf-8")
common_json_data = json.load(common_json_file)
c = open("common_events.rpy","w",encoding="utf-8")

system_file = open("System.json")
system_file = json.load(system_file)

map_file = open("Mapinfos.json")
json_map = json.load(map_file)

common_count = 0

for common_event in common_json_data:
    if common_json_data[common_count] is not None:
        label_name = common_json_data[common_count]["name"]
        common_label = "common_"+label_name
        pattern = r'[^A-Za-z0-9_ ]+'
        common_label = re.sub(pattern, '', str(common_label)).lower()
        if common_count >1:
            c.writelines('    return\n')
        c.writelines('\nlabel {}:\n'.format(common_label.replace(" ","_")))
        padding = 0
        for common_list in common_json_data[common_count]["list"]:
            code = str(common_list["code"])
            if code == "111":
                if common_list["parameters"][0] == 1:
                    params = ['==', '>=', '<=', '>', '<', '!=']
                    variable_name = system_file["variables"][common_list["parameters"][1]]
                    variable_params = int(common_list["parameters"][4])
                    
                    numerator = str(params[variable_params])
                    variable_comperator = str(common_list["parameters"][3])
                    #if padding == 0:
                    
                    variable_name = re.sub(pattern, '',variable_name).lower()
                    variable_name = variable_name.replace(" ","_")
                    c.writelines("  "*padding+"    if {} {} {}:\n".format(variable_name,numerator,variable_comperator))
                    padding += 2
                elif common_list["parameters"][0] == 0:
                    on_off = ["on","off"]
                    on_off_value = int(common_list["parameters"][2])
                    #if padding == 0:
                    switch_name = system_file["switches"][int(common_list["parameters"][1])]
                    switch_name = re.sub(pattern,'',str(switch_name))
                    switch_name = switch_name.replace(" ","_").lower()
                    c.writelines('  '*padding+'    if switch_{} == "{}":\n'.format(switch_name,on_off[on_off_value]))
                    padding += 2
            if code == "231":
                scene_name = common_list["parameters"][1]
                #if padding == 0:
                c.writelines("  "*padding+"    scene {}\n".format(scene_name))
                
            if code == "101":
                char_name = common_list["parameters"][0]
                character_name = str(char_name).strip()
                #c.writelines("\n  {} ".format(character_name))
            if code == "401":
                dialogue = common_list["parameters"][0]
                if character_name == "":
                    #if padding == 0:
                    c.writelines('  '*padding+'    "{}"\n'.format(dialogue))
                    
                else:
                    #if padding == 0:
                    c.writelines('  '*padding+'    {} "{}"\n'.format(character_name,dialogue))
            if code == "122":
                if common_list["parameters"][3] == 0:
                    set_variable_name = system_file["variables"][common_list["parameters"][1]]
                    set_variable_value = common_list["parameters"][4]
                    set_variable_name = re.sub(pattern,'',set_variable_name)
                    set_variable_name = set_variable_name.replace(" ","_").lower()
                    c.writelines("  "*padding+"    $ {} = {}\n".format(set_variable_name,set_variable_value))
                    
            if code == "121":
                on_off = ["on","off"]
                set_switch_name = system_file["switches"][int(common_list["parameters"][1])]
                true_false_value = on_off[common_list["parameters"][2]]
                #if padding == 0:
                set_switch_name = re.sub(pattern,'',str(set_switch_name).lower())
                set_switch_name = set_switch_name.replace(" ","_")
                c.writelines('  '*padding+'    $ switch_{} = "{}"\n'.format(set_switch_name,true_false_value))
                
            if code == "201":
                set_map_num = common_list["parameters"][1]
                try:
                    set_map_name = json_map[set_map_num]["name"]
                except:
                    c.writelines("  "*padding+"    #trying map {}".format(set_map_name))
                #if padding == 0:
                c.writelines("  "*padding+"    call {}\n".format(set_map_name))
                
            if code == "411":
                #if padding == 0:
                c.writelines("  "*padding+"    else:\n")
                padding += 2
                #else:
                #    c.writelines("    {}".format(padding))
            if code == "0":
                padding -= 2
            if code == "355":
                variable_set = common_list["parameters"][0]
                variable_type = variable_set.split(".")
                if variable_type[0] == "$gameVariables":
                    if "(" in str(variable_set):
                        variable_name = variable_set.split("(")
                        variable_number = variable_name[1].split(",")[0]
                        variable = system_file["variables"][int(variable_number)]
                        if '"' in variable_set:
                            variable_value = variable_set.split('"')
                            variable = re.sub(pattern, '',str(variable))
                            variable = variable.replace(" ","_").lower()
                            c.writelines('  '*padding+'    $ {} = "{}"\n'.format(variable,variable_value[1]))
                            #modify_variables(variable,variable_value[1])
                elif variable_type[0] == "ysp":
                    if "(" in str(variable_set):
                        if "newVideo" in str(variable_set):
                            video_name = variable_set.split("'")[1]
                            c.writelines("  "*padding+"    #play video {}\n".format(video_name))
            if code == "117":
                common_event_num = common_list["parameters"][0]
                common_event_label_name = re.sub(pattern,'',common_json_data[common_event_num]["name"])
                common_event_label_name = common_event_label_name.replace(" ","_")
                c.writelines("  "*padding+"    call {}\n".format("common_events_"+common_event_label_name.lower()))
            if code == "118":
                sub_label_name = common_label+common_list["parameters"][0]
                sub_label_name = re.sub(pattern,'',sub_label_name)
                sub_label_name = sub_label_name.replace(" ","_").lower()
                c.writelines("  "*padding+"    label {}:\n".format(sub_label_name))

    common_count+=1

def clean_string(input_string):
    # This regex pattern keeps only a-z, A-Z, 0-9, _ and -
    return re.sub(r'[^a-zA-Z0-9_-]', '', input_string)

#print ("common_id::",common_json_data[664]["name"])
ev = open("./events_list/events_list.rpy","w",encoding="utf-8")

for x in range(1,38):
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


    
    #print (json_map[map_num]["name"])
    map_name = json_map[map_num]["name"].replace(" ", "_")
    name_pattern =  r'[^A-Za-z0-9_]+'
    map_name = str(re.sub(name_pattern,'',map_name)).lower()
    print (map_name)

    f = open("{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")
    sayers = open("sayer.rpy","w",encoding="utf-8")

    #ev = open("./events_list/events_list_{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")
    #switch_data = 
    with open("switches_with_labels_list.json", "r",encoding="utf-8") as switch_json:
        switch_data = json.load(switch_json)
    #switch_entries = {list(entry.keys())[0]: entry for entry in switch_data}
    count = 0
    for events in json_data["events"]:
        
        if json_data["events"][count] is not None:
            event_id = json_data["events"][count]["id"]
            event_name = json_data["events"][count]["name"]
            event_note = json_data["events"][count]["note"]
            label_name = str(map_name)+"_"+str(event_name)+str(event_note)+"_"+str(event_id)
            
            character_name = ""
            page_count = 0
            for pages in json_data["events"][count]["pages"]:
                padding = 0
                switch_id = pages["conditions"]["switch1Id"]
                switch = system_file["switches"][switch_id]
                switch_bool = pages["conditions"]["switch1Valid"]

                switch_id2 = pages["conditions"]["switch2Id"]
                switch2 = system_file["switches"][switch_id2]
                switch_bool2 = pages["conditions"]["switch2Valid"]

                label = label_name+"_"+str(page_count)
                pattern = r'[^A-Za-z0-9_ ]+'
                label = re.sub(pattern, '', str(label)).lower()
                
                switch = re.sub(pattern, '',switch)
                switch = str(switch).replace(" ","_").lower()

                switch2 = re.sub(pattern, '',switch2)
                switch2 = str(switch2).replace(" ","_").lower()

                if count >1:
                    f.writelines("    return\n")
                f.writelines('\nlabel {}: '.format(label.replace(" ","_")))
                ev.writelines('\nlabel {}: '.format(label.replace(" ","_")))

                page_count+=1
                if switch.endswith('_'):
                    switch = switch[:-1]
                f.writelines("    #switch1: {} = {} ".format(switch,switch_bool))
                ev.writelines("    #switch1: {} = {} ".format(switch,switch_bool))
                print(switch)
                if switch_bool == True:
                    switch_data[f"switch_{switch}"].append(label.replace(" ","_"))
                
                if switch2.endswith('_'):
                    switch2 = switch2[:-1]
                f.writelines("    #switch2: {} = {} ".format(switch2,switch_bool2))
                ev.writelines("    #switch2: {} = {} ".format(switch2,switch_bool2))
                if switch_bool2 == True:
                    switch_data[f"switch_{switch2}"].append(label.replace(" ","_"))

                variable_id = pages["conditions"]["variableId"]
                variable_value = pages["conditions"]["variableValue"]
                variable = system_file["variables"][variable_id]
                variable = variable.replace(" ","_")
                variable = re.sub(pattern, '',variable).lower()
                variable = clean_string(variable)
                f.writelines("    #variables: {} = {} ".format(variable,variable_value))
                ev.writelines("    #variables: {} = {} ".format(variable,variable_value))

                trigger = pages["trigger"]
                trigger_list = ["action_button","player_touch","event_touch","autorun","parallel"]
                label_trigger = trigger_list[int(trigger)]
                f.writelines("    #trigger: {}\n".format(label_trigger))
                ev.writelines("    #trigger: {}\n".format(label_trigger))
                
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
                            variable_name = clean_string(variable_name)
                            f.writelines("  "*padding+"    if {} {} {}:\n".format(variable_name,numerator,variable_comperator))
                            padding += 2
                        elif per_list["parameters"][0] == 0:
                            on_off = ["on","off"]
                            on_off_value = int(per_list["parameters"][2])
                            #if padding == 0:
                            switch_name = system_file["switches"][int(per_list["parameters"][1])]
                            switch_name = re.sub(pattern,'',str(switch_name))
                            switch_name = switch_name.replace(" ","_").lower()
                            switch_name = clean_string(switch_name)
                            f.writelines('  '*padding+'    if switch_{} == "{}":\n'.format(switch_name,on_off[on_off_value]))
                            padding += 2
                    if code == "231":
                        scene_name = per_list["parameters"][1]
                        scene_name = str(scene_name.replace(" ","_"))
                        scene_name = scene_name.replace("'","_")
                        scene_name = scene_name.replace(")","")
                        scene_name = scene_name.replace("(","")
                        scene_name = clean_string(scene_name)
                        #if padding == 0:
                        f.writelines("  "*padding+"    scene {}\n".format(scene_name.lower()))
                        
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
                            set_variable_name = clean_string(set_variable_name)
                            f.writelines("  "*padding+"    $ {} = {}\n".format(set_variable_name,set_variable_value))
                            ev.writelines("  "*padding+"    $ {} = {}\n".format(set_variable_name,set_variable_value))
                            
                    if code == "121":
                        on_off = ["on","off"]
                        set_switch_name = system_file["switches"][int(per_list["parameters"][1])]
                        true_false_value = on_off[per_list["parameters"][2]]
                        #if padding == 0:
                        set_switch_name = re.sub(pattern,'',str(set_switch_name).lower())
                        set_switch_name = set_switch_name.replace(" ","_")
                        set_switch_name = clean_string(set_switch_name)
                        f.writelines('  '*padding+'    $ switch_{} = "{}"\n'.format(set_switch_name,true_false_value))
                        ev.writelines('  '*padding+'    $ switch_{} = "{}"\n'.format(set_switch_name,true_false_value))
                        #modify_variables(set_switch_name,true_false_value)
                        
                    if code == "201":
                        set_map_num = per_list["parameters"][1]
                        try:
                            set_map_name = json_map[set_map_num]["name"]
                        except:
                            f.writelines("  "*padding+"    #trying map {}".format(set_map_name))
                        #if padding == 0:
                        set_map_name = clean_string(set_map_name)
                        f.writelines("  "*padding+"    call {} #map\n".format(set_map_name.lower().replace(" ","_").replace("-","")))
                        ev.writelines("  "*padding+"    call {} #map\n".format(set_map_name.lower().replace(" ","_").replace("-","")))
                        
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
                                    variable = variable.replace(" ","_").lower()
                                    variable = clean_string(variable)
                                    f.writelines('  '*padding+'    $ {} = "{}"\n'.format(variable,variable_value[1]))
                        elif variable_type[0] == "ysp":
                            if "(" in str(variable_set):
                                if "newVideo" in str(variable_set):
                                    video_name = variable_set.split("'")[1]
                                    video_name = clean_string(video_name)
                                    f.writelines("  "*padding+"    #play video {}\n".format(video_name))
                    if code == "117":
                        common_event_num = per_list["parameters"][0]
                        common_event_label_name = re.sub(pattern,'',common_json_data[common_event_num]["name"])
                        common_event_label_name = common_event_label_name.replace(" ","_")
                        common_event_label_name = clean_string(common_event_label_name)
                        f.writelines("  "*padding+"    call {}\n".format("common_"+common_event_label_name.lower()))
                        ev.writelines("  "*padding+"    call {}\n".format("common_"+common_event_label_name.lower()))
                    if code == "118":
                        sub_label_name = label+per_list["parameters"][0]
                        sub_label_name = re.sub(pattern,'',sub_label_name)
                        sub_label_name = sub_label_name.replace(" ","_").lower()
                        sub_label_name = clean_string(sub_label_name)
                        f.writelines("  "*padding+"    label {}:\n".format(sub_label_name))
                        ev.writelines("  "*padding+"    label {}:\n".format(sub_label_name))

        count+=1    

        #for json_list in json_data["events"][count]["pages"]:
        #    print(json_list["conditions"])

    with open("switches_with_labels_list.json", "w", encoding="utf-8") as switch_json:
        json.dump(switch_data, switch_json, indent=4, ensure_ascii=False)

in_path = '../img/pictures/'

out_path = './images/'
if not os.path.exists(out_path):
    # Create the new folder
    os.makedirs(out_path)

for file in os.listdir(in_path):
    file_name = str(file.replace(" ","_"))
    file_name = file_name.replace("'","_")
    file_name = file_name.replace(")","")
    file_name = file_name.replace("(","")
    os.rename(in_path + file, out_path + file_name.lower())

then = os.listdir(out_path)
print("copying the ../img/pictures to ./images")
