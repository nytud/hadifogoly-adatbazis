import re

# abbrs_transcribed_dict = {
#     'EMPTY': 'country',
#     'NUMBER': 'number',
#     'obl.': 'county',
#     'r-n': 'county',  # ha nincs obl./okr., akkor megye, különben járás
#     'okr.': 'county',
#     'gub.': 'county',
#     'kr.': 'county',
#     'u.': 'county',
#     'pr.': 'county',
#     'prov.': 'county',
#     'k.': 'county',
#     'o.': 'county',  # megye / kevesebbszer város
#     'g.': 'city',
#     'sz.': 'city',
#     'szl.': 'city',
#     'r.': 'city',
#     'm.': 'district',
#     'd.': 'village',  # falu vagy község vagy házszám (kisebb számban)
#     'szt.': 'city',
#     'ul.': 'street'}

pat_num = re.compile(r'\d+')

scale_of_types = ['country', 'county', 'district', 'city', 'street']

scale_of_types_all = ['country', 'county', 'district', 'city', 'village', 'street', 'number']

frequent_countries = ['Венгр.',
                      'Венг.',
                      'Венгрии',
                      'Венгрия',
                      'Австрия',
                      'Австрии',
                      'Чехословак.',
                      'Чехослов.',
                      'Чехословакия',
                      'Чехословакии',
                      'Словакия',
                      'Словакии',
                      'Словак.',
                      'Германия',
                      'Германии',
                      'Румыния',
                      'Румынии',
                      'Югославия',
                      'Югославии',
                      'Польша'] # Lengyelország

abbrs_rus_dict = {
    'EMPTY': 'country',
    'NUMBER': 'number',
    'обл.': 'county',  # megye
    'р-н': 'county',  # megye, ha van obl, akkor ált. város/község
    'окр.': 'county',  # megye
    'губ.': 'county',  # megye/tartomány
    'кр.': 'county',  # megye
    'у.': 'county',  # megye
    'уезд': 'county',
    'у-д': 'county',
    'пр.': 'county',  # megye
    'пров.': 'county',  # megye
    'к.': 'county',  # megye
    'о.': 'county',  # megye / kevesebbszer város
    'г.': 'city',  # város
    'с.': 'city',  # város
    'сл.': 'city',  # város
    'р.': 'city',  # város
    'м.': 'district',  # város/község
    'д.': 'village',  # község vagy házszám (kisebb számban)
    'ул.': 'street',  # utca
    'ст.': 'city'}  # város


def extract_location_parts(string):
    location_parts = {
        "country": '',
        "county": '',
        "district": '',
        "city": '',
        "village": '',
        "street": '',
        "number": ''
    }

    # a stringből (ami egy mező tartalma) kiszedett hely-elemeket beletesszük
    # egy dict-be (olyan key-ekkel, amit a json példában írtam),
    # és visszaadjuk a dict-et

    locations_per_string = []
    current_abbreviations = set()

    # általában vesszővel vannak elválasztva egymástól a különböző típusú helyinformációk
    # ezekben keresem a rövidítés szótárakban lévő rövidítéseket és azonosítom a típust
    for location_info in string.replace(', ', ',').split(','):
        location_info = location_info.strip()
        current_abbreviation = ''
        number = pat_num.search(location_info)
        if number:
            current_location_type = abbrs_rus_dict['NUMBER']
            locations_per_string.append((current_location_type, current_abbreviation, number.group()))
            continue

        current_location_info = location_info.split()
        current_location_type = abbrs_rus_dict['EMPTY']

        for poss_abbreviation in current_location_info:
            poss_abbreviation = poss_abbreviation.lower()
            if poss_abbreviation in abbrs_rus_dict.keys():
                current_abbreviation = poss_abbreviation
                current_abbreviations.add(poss_abbreviation)

                location_info = location_info.replace(current_abbreviation, '')
                current_location_type = abbrs_rus_dict[current_abbreviation]

        locations_per_string.append((current_location_type, current_abbreviation, location_info.strip()))

    # Ha nincsen rövidítés a sorban, de csak kettő elemből áll, akkor gyakran ország, város információt tartalmaz a sor
    if len(current_abbreviations) == 0 and len(locations_per_string) == 2 \
            and locations_per_string[0][0] != 'number' and locations_per_string[1][0] != 'number':
        if locations_per_string[0][2] in frequent_countries and not locations_per_string[1][2].endswith('меде'):
            location_parts[locations_per_string[0][0]] = locations_per_string[0][2]
            location_parts['city'] = locations_per_string[1][2]
            return location_parts

        elif locations_per_string[1][2] in frequent_countries and not locations_per_string[0][2].endswith('меде'):
            location_parts[locations_per_string[1][0]] = locations_per_string[1][2]
            location_parts['city'] = locations_per_string[0][2]
            return location_parts

    # Miután megvannak a rövidítések és a hozzájuk tartozó információk, el kell végezni
    # egy utolagos információ-típus ellenőrzést.
    # pl. az r-n nagyon sokszor megyét jelöl,
    # persze ha van mellette explicit megye (obl./okr.),
    # akkor nem megyét, hanem valóban járást jelöl
    #print(locations_per_string)
    current_location_types = [location_infos[0] for location_infos in locations_per_string]
    for i, (loc_type, abbr, info) in enumerate(locations_per_string):
        stop = False
        if (abbr == 'р-н' and current_location_types.count('county') > 1) \
                or (abbr == 'г.' and current_location_types.count('city') > 1):

            del current_location_types[current_location_types.index(loc_type)]
            loc_type = 'district'
            locations_per_string[i] = (loc_type, abbr, info)
            current_location_types.append(loc_type)

        elif loc_type != 'number' and loc_type != 'village' and loc_type != 'county' and abbr != 'с.' \
                and info not in frequent_countries \
                and (current_location_types.count(loc_type) > 1 or loc_type == 'country'):
            #print(info, loc_type)
            if loc_type == 'country':
                loc_type = 'county'
                current_location_types.append(loc_type)
                del current_location_types[current_location_types.index('country')]
                if current_location_types.count(loc_type) == 1:
                    stop = True
            if not stop:
                temp_loc_type = loc_type
                # A tendency azt nézi, hogy milyen hierarchiában követik egymást az információk, kisebbtől a nagyobb
                # halmaz felé vagy fordítva
                tendency = scale_of_types_all.index(locations_per_string[0][0]) - scale_of_types_all.index(loc_type)
                if tendency < 0:
                    tendency = 1
                elif tendency > 0 or tendency == 0:
                    tendency = -1
                if scale_of_types.index(loc_type) + tendency + 1 > len(scale_of_types):
                    stop = True
                if not stop:
                    if scale_of_types[scale_of_types.index(loc_type) + tendency] not in current_location_types:
                        loc_type = scale_of_types[scale_of_types.index(loc_type) + tendency]
                    while loc_type in current_location_types:
                        if scale_of_types.index(loc_type) + 1 == len(scale_of_types):
                            break
                        loc_type = scale_of_types[scale_of_types.index(loc_type) + 1]
                    current_location_types.append(loc_type)
                    del current_location_types[current_location_types.index(temp_loc_type)]
        if location_parts[loc_type] == '':
            location_parts[loc_type] = info
        else:
            for key in location_parts:
                if location_parts[key] == '':
                    location_parts[key] = info
                    break
    #print(location_parts)
    #print()
    return location_parts


def main():
    # test_ls = []
    # for line in test_ls:
    #     string = line.strip()
    #     extract_location_parts(string)
    # with open('../data/Kart_1000_Sor.csv', encoding='utf-8') as inputf:
    # with open('../out/Kart.csv.fejes.transcribed', encoding='utf-8') as inputf:

    with open('../data/Kart.csv', encoding='utf-8') as inputf:

        for line in inputf:
            string = line.strip().split('\t')
            if len(string) < 7:
                return None
            # extract_location_parts(string[5])
            # extract_location_parts(string[6])
            print(extract_location_parts(string[5]))
            print(extract_location_parts(string[6]))


if __name__ == '__main__':
    main()
