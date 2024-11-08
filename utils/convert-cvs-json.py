""" convert the exiting database csv to json"""
import uuid
import csv
import json


person_list = []
family_list = []
parent_list = []
member_list = []

def read_ods_to_dicts():
    """ Read the file .ods(csv) to dictionaries."""
    # Read person list
    rpl = ["person", "id", "lastname", "firstname", "call_name", "suffix", "prefix",
           "title", "sex", "birthday", 'birth place', 'birth source', "baptism date",
           "baptism place", "baptism source", "death date", "death place", "death source",
           "burial date", "burial place", "burial source", "note"]
    # read family list
    rfl = ["family", "father", "mother", "date", "place"]
    drop_list = ["suffix", "prefix", "title", 'birth place', 'birth source', "baptism date",
           "baptism place", "baptism source", "death date", "death place", "death source",
           "burial date", "burial place", "burial source", "note"]
    month_dict = dict(JAN='01', FEB='02', MAR='03', APR='04',  MAY='05', JUN='06',
                    JUL='07', AUG='08', SEP='09', OKT='10', NOV='11', DEC='12')

    # read the data in person_dict
    with open("utils/Spierings_02.csv") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=rpl)
        # row = psr
        for row in reader:
            row["id"] = str(uuid.uuid4())
            row["birthday_txt"] = ''
            row["father"] = ""
            row["mother"] = ""
            if row['prefix'] != '':
                row['lastname'] = f"{row['prefix'].strip()} {row['lastname']}"
            # Check the birthday format type date is required other to birthday_txt
            if row["birthday"] != '':
                if len(row["birthday"].strip()) <= 4:
                    row["birthday_txt"] = row["birthday"]
                    row["birthday"] = ""
                # convert month format if not YYYY-MM_DD
                if row["birthday"][-4:].isalnum():
                    year = row["birthday"][-4:]
                    # print(f"month: {row["birthday"][-8:-5]}")
                    month = month_dict[row["birthday"][-8:-5]]
                    day = row["birthday"][:2].strip()
                    if len(day) == 1:
                        day = f"0{day}"
                    row["birthday"] = f"{year}-{month}-{day}"
                    row["birthday_txt"] = year
            row["sex"] = row["sex"][0].capitalize()
            # drop all not required fields
            for key in drop_list:
                row.pop(key)
            person_list.append(row)

    # make a list of old id to the uuid
    id_list = []
    for dic in person_list:
        row = [dic["person"], dic["id"]]
        id_list.append(row)

    # read the family (married) db convert the id to uuid
    with open("utils/Spierings_family.csv") as csvf:
        reader = csv.DictReader(csvf, fieldnames=rfl)
        for row in reader:
            for i, u in id_list:
                if i == row["mother"]:
                    row["mother"] = u
                if i == row['father']:
                    row['father'] = u
            family_list.append(row)

    # Read the family from the child convert to father and mother
    # and fill it in in the person_list
    with open("utils/Spierings_child.csv") as fcsv:
        reader = csv.DictReader(fcsv, ["Fam", "Person"])
        for row in reader:
            family = row["Fam"]
            person = row["Person"]
            for list in family_list:
                if family == list["family"]:
                    father = list["father"]
                    mother = list["mother"]
                    break   # found it no need to carry on.

            for row in person_list:
                if person == row["person"]:
                    row["father"] = father
                    row["mother"] = mother
                    break

    # 'person' Is not needed anymore
    # Make a new list of dictionaries

    for row in person_list:

        member = row.copy()
        del member['person']
        member_list.append(member)

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open("utils/Spierings_json.json", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(member_list, indent=4))


if  __name__ == "__main__":
    # All required files are in code
    read_ods_to_dicts()

