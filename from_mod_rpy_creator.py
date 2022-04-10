import re
import os

cwd = os.getcwd()
#print(cwd)
test_line = "# --- 0.5: Разговор с мамой Кати насчёт денег ($5000)|Conversation with Kate's mom about $5000"
#print (":::",test_line[0])
file_name="voyeur.txt"
#file_name="test.txt"
file_name_without_ext=file_name.split(".")[0]

#f = open("{pwd}\\{fn}rpy.txt".format(fn=file_name_without_ext,pwd=cwd), "w")
f = open("{fn}.rpy".format(fn=file_name_without_ext),"w",encoding="utf-8")
#f = open("./erictalk.rpy","w")
#f.write("a")

def print_sayer(spoker_num):
    #=================================================================================================================
    # get characters name from [D:\apps_n_files\Big Brother Renpy Remake Story Version 0.1\game\images\character]
    #=================================================================================================================
    if spoker_num>=0 and spoker_num <=17:
    #print ("max")
        f.writelines("  max")
    if spoker_num>=20 and spoker_num<=39:
        f.writelines("  alice")
    if spoker_num>=40 and spoker_num<=50:
        f.writelines("  lisa")
    if spoker_num>=60 and spoker_num<=79:
        f.writelines("  mom")
    if spoker_num>=80 and spoker_num<=95:
        f.writelines("  eric")
    if spoker_num>=100 and spoker_num<=114 or spoker_num == 124:
        f.writelines("  aunt")
    if spoker_num>=120 and spoker_num<=125 and spoker_num !=124:
        f.writelines("  max")
    if spoker_num>=311 and spoker_num<=319:
        f.writelines("  max")
    if spoker_num>=333 and spoker_num<=337:
        f.writelines("  aunt")
    if spoker_num>=340 and spoker_num<=346:
        f.writelines("  lisa")
    if spoker_num>=350 and spoker_num<=356:
        f.writelines("  aunt")
    if spoker_num>=360 and spoker_num<=363:
        f.writelines("  mom")
    if spoker_num>=150 and spoker_num<=159:
        f.writelines("  cousin")
    if spoker_num>=140 and spoker_num<=149:
        f.writelines("  olivia")

line_num=1
with open(file_name, encoding="utf-8") as text_file:
    non_blank_lines = [line.strip() for line in text_file if line.strip()]
    for line in non_blank_lines:
        length_of_line = len(line)
        line=line.strip()
        #print (length_of_line)
        if length_of_line <2:
            continue
        if length_of_line>=2:
            if line[0] == "#" and line[1] != "#" or line_num==1:
                line_num+=1
                line_with_or = line.split("|")
                if "|" in line:
                    #print (line_with_or[1])
                    label_with_underscore = line_with_or[1].strip().replace(" ","_")
                    pattern = r'[^A-Za-z0-9_]+'
                    label_without_special_char = re.sub(pattern, '', label_with_underscore)
                    #print("label::",label_without_special_char)
                    #print(label_without_special_char[0])    
                    if label_without_special_char[0].isdigit():
                        new = list(label_without_special_char)
                        new[0] = 'max_'
                        label_without_special_char = ''.join(new)
                        print (label_without_special_char)
                        f.writelines("\nlabel  {}: \n".format(label_without_special_char))
                        continue
                    f.writelines("\nlabel  {}: \n".format(label_without_special_char))
                continue
            if line[0] == "#" and line[1] == "#":
                #print("ignoring line::",line)
                continue
            if "@" in line:
                #print (line)
                if line.count('@') == 1:
                    #print ("ignoring"+line)
                    continue
                line_with_at = line.split("@")
                if "|" not in line_with_at[2]:
                    #print ("scene "+line_with_at[2])
                    if "anim" in line_with_at[2]:
                        print ("skiping animations")
                        print (line_with_at[2])
                        f.writelines('  "animation here {}"\n'.format(line_with_at[2]))
                        continue
                    if "anim" not in line_with_at[2]:
                        f.writelines("  scene "+line_with_at[2]+"\n")
                    #print (line_with_at[1])
                    #print ("img")
                if "|" in line:
                    line_with_or = line.split("|")
                    #print ('\"'+line_with_or[1]+'\"')
                    #print(line_with_or)
                    spoker_num = int(line_with_at[1])
                    #if spoker_num.isdigit():
                    print_sayer(spoker_num)
                    dialogue=line_with_or[1].strip()
                    dialogue_without_quotes=dialogue.replace('"',"'")
                    dialogue_without_quotes=dialogue_without_quotes.replace("[","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("]","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("(","")
                    dialogue_without_quotes=dialogue_without_quotes.replace(")","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("<color=orange>","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("<color=lime>","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("</color>","")
                    dialogue_without_quotes=dialogue_without_quotes.replace("%","percent")
                    #pattern = r'[^A-Za-z0-9_]+'
                    #dialogue_without_special_char = re.sub(pattern, '', dialogue_without_quotes)
                    f.writelines('  \"{}\"\n'.format(dialogue_without_quotes))
                    #f.close()
                    continue
                continue
            if "|" in line and "@" not in line and line[0] != "#" and line_num != 1:
                #print (line,"::and::",line[1])
                line_with_or_and_not_at = line.split("|")
                dialogue=line_with_or_and_not_at[1].strip()
                dialogue_without_quotes=dialogue.replace('"',"'")
                dialogue_without_quotes=dialogue_without_quotes.replace("[","")
                dialogue_without_quotes=dialogue_without_quotes.replace("]","")
                dialogue_without_quotes=dialogue_without_quotes.replace("(","")
                dialogue_without_quotes=dialogue_without_quotes.replace(")","")
                dialogue_without_quotes=dialogue_without_quotes.replace("<color=orange>","")
                dialogue_without_quotes=dialogue_without_quotes.replace("<color=lime>","")
                dialogue_without_quotes=dialogue_without_quotes.replace("</color>","")
                dialogue_without_quotes=dialogue_without_quotes.replace("=","")
                dialogue_without_quotes=dialogue_without_quotes.replace("%","percent")
                #print(line_with_or_and_not_at[1])
                f.writelines('  max  \"{}"\n'.format(dialogue_without_quotes))
            continue
            
            