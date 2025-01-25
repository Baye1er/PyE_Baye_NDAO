import csv
import re

# Below, are functions to be used the program
def classe_func(cl):
    cl = str(cl)
    cl = cl.split(" ")
    cl = "".join(cl)
    return cl

def processString5(txt):
    transTable = txt.maketrans("èmé", "eme")
    txt = txt.translate(transTable)
    return txt

def replaceEmeinEm(text):
    text = text.replace('eme', 'em')
    text = text.replace('em', 'em ')
    return text

####### ******** Function returning the average of each subject and the global average for all of them ******** #########
def moyenne(liste):
    # liste = "[Math[04;03:05]#Francais[15;16:14]#Anglais[15;16:14]#PC[04;03:07]#SVT[12;09:15]#HG[16;15:13]]"
    liste1 = liste.split("#")
    # key_list = ['name', 'age', 'address']
    # value_list = ['Johnny', '27', 'New York']
    # dict_from_list = dict(zip(key_list, value_list))
    # print(dict_from_list)
    keys_list = ["PC", "Math", "Français", "Anglais", "SVT", "HG"]
    values_list = []
    liste_moy = []
    for i in liste1:
        regex = "\d+"
        match = re.findall(regex, str(i))
        values_list.append(list(map(int, match)))
    for j in values_list:
        l = list(j)
        ls = l[:(len(l)-1)]
        m = sum(ls)/(len(l)-1)
        moy = (m+(l[-1])*2)/3
        liste_moy.append(moy)
    mg = sum(liste_moy)/len(liste_moy)
    dict_moy = {"Moyenne Generale": mg}
    dict_from_list = dict(zip(keys_list, liste_moy))
    dict_from_list1 = {**dict_from_list, **dict_moy}
    return dict_from_list1

########## Function to be used for re-formatting the date ##########
def format_date(deux):
    from datetime import datetime
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y','%d.%m.%Y','%d,%m,%Y','%Y-%d-%m', '%Y-%d-%b',
                '%d-%b-%Y', '%d/%b/%Y','%d.%b.%Y'):
        try:
            date = datetime.strptime(deux, fmt)
            nouv_date = date.strftime('%d-%m-%Y')
        except ValueError:
                            continue
        return nouv_date
######################  ******* Main Program ******* #############################
with open('project_data.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open('csv_file.csv', 'w') as new_file:
        fieldnames = ['Numero', 'Nom', 'Prénom', 'Date de naissance', 'Classe', 'Note']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter = '\t')
        csv_writer.writeheader()
        valid_list = []
        finalInvalidData = []
        for line in csv_reader:
            del line['CODE']
            # Rename the variables for best practice
            num = line['Numero']
            nom = line['Nom']
            prenom = line['Prénom']
            date = line['Date de naissance']
            classe = line['Classe']
            note = line['Note']
            if line['Numero'] != '' and line['Note'] != '':
                if num == num.upper() and len(num) == 7 and num.isalnum():
                    if nom[0].isalpha() and len(nom) >= 2:
                        if prenom[0].isalpha() and len(prenom) >= 3:
                            csv_writer.writerow(line)
                            valid_list.append(line)
            else:
                finalInvalidData.append(line)

###### ********** Data handling of the valid list ********** #######
finalValidData = []
invalidData = []
for liste in valid_list:
    liste['Date de naissance'] = format_date(liste['Date de naissance'])
    liste['Classe'] = classe_func(liste['Classe'])
    liste['Classe'] = processString5(liste['Classe'])
    try:
        liste['Note'] = moyenne(liste['Note'])
    except IndexError:
        continue
    if liste['Date de naissance'] != None:
        if liste['Classe'] in ['6emeA', '6emeB', '6emA', '6emB', '5emeA', '5emeB',
                                   '5emA', '5emB', '4emeA', '4emeB', '4emA', '4emB', '3emeA', '3emeB', '3emA', '3emB']:
            liste['Classe'] = replaceEmeinEm(liste['Classe'])
            finalValidData.append(liste)  # the finalValidData container contains the list of the valid data
    else:
        invalidData.append(liste)

for falsedata in invalidData:
    finalInvalidData.append(falsedata)  # the finalInvalidData container contains the list of invalid data

#for i in finalValidData:
 # print(i)
#for row in finalInvalidData:
 #  print(row)

####################### *************** Below, is the code of the menu ******************** ###############################
print("- List of valid data, enter : 1")
print("- List of invalid data, enter : 2")
val = int(input('Entrer ...'))
if val == 1:
   for row in finalValidData:
       print(row)
if val == 2:
    for r in finalInvalidData:
        print(r)

############### Search element with its number ####################
numero = input("Search an element over here with its number:")
if numero == liste['Numero']:
    print(liste)
else:
    print('No line matchs to the number: {}'.format(numero))

#################### *************** Display the 5 top ranking students ******************* #############################
# test