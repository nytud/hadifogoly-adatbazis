import re
import sys


"""
Jelenleg ezt a négy típust keresi és adja ki a program, amennyiben jelen vannak egy sorban:
country - ország
county - megye
district - járás
city - város
"""

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

# todo: ha kell (argumentum alapján), akkor egy típusból többet is visszaad, ha több rövidítés van
#  egy típusból


scale_of_types = ['county', 'district', 'city']  # street]

county_hint_words = {'меде', 'меди', 'медя'}

frequent_countries = [
    # 'Венгр.',
    # 'Венг.',
    # 'Венгрии',
    'Венгрия',
    'Австрия',
    # 'Австрии',
    # 'Австр.',
    # 'Чехословак.',
    # 'Чехослов.',
    'Чехословакия',
    # 'Чехословакии',
    'Словакия',
    # 'Словакии',
    # 'Словак.',
    'Германия',
    # 'Германии',
    'Румыния',
    # 'Румынии',
    'Югославия',
    # 'Югославии',
    'Трансильвания',
    'Польша',
    'Чехия',
    'Силезия',
    'Галиция',
    'Дания',
    'Бессарабия',
    'Белоруссия',
    'Латвия',
    'Болгария'
]

# Abban az esetben kikommentelendő, ha a számokat is fel szeretnénk dolgozni
# poss_districts = {'р-н', 'p-нe', 'р-он', 'р-на', 'кр.', 'к.', 'у.', 'уезд', 'у-д'}

abbrs_rus_dict = {
    'обл.': 'county',  # megye
    'окр.': 'county',  # megye
    'о.': 'county',  # megye / kevesebbszer város
    'ок.': 'county',
    'губ.': 'county',  # megye/tartomány
    'пр.': 'county',  # megye
    'пров.': 'county',  # megye
    'прав.': 'county',
    'кр.': 'county',  # megye
    'к-р': 'county',  # megye
    'к.': 'county',  # megye
    'край': 'county',
    'комитат': 'county',
    'к-т': 'county',
    'р-н': 'county',  # megye, ha van obl, akkor ált. város/község
    'p-нe': 'county',  # ua., mint egyel feljebb
    'р-он': 'county',
    'р-на': 'county',
    'у.': 'county',  # megye
    'уезд': 'county',
    'у-д': 'county',
    'ком.': 'county',  #  уезд után inkáb disctrict, míg a komitat nem.
    'м.': 'district',  # város/község
    'с.': 'city',  # város
    'ст.': 'city',  # város
    'д.': 'city',  # község vagy házszám (kisebb számban)
    'г.': 'city',  # város ez lehet disctrict is
    'сл.': 'city',  # város
    'р.': 'city',  # város
    # 'ул.': 'street'  # utca
}


def extract_location_parts(string, row_num=None):
    location_parts = {
        # "raw_num": row_num,  # only for test
        "country": '',
        "county": '',
        "district": '',  # járás
        "city": '',
        "village": '',
        "street": '',
        "number": ''
    }

    # a stringből (ami egy mező tartalma) kiszedett hely-elemeket beletesszük
    # egy dict-be (olyan key-ekkel, amit a json példában írtam),
    # és visszaadjuk a dict-et

    locations_per_string = []
    abbreviations = set()

    # Általában vesszővel vannak elválasztva egymástól a különböző típusú helyinformációk
    # ezekben keresem a rövidítés szótárakban lévő rövidítéseket és azonosítom a típust

    is_country_found = False
    for location_info in string.replace(', ', ',').split(','):
        for county_hint_word in county_hint_words:
            location_info = location_info.replace(f' {county_hint_word}', county_hint_word)
            location_info = location_info.replace(f'-{county_hint_word}', county_hint_word)

        location_info = location_info.strip()
        abbreviations_per_locaton = set()

        current_location_info = location_info.split()
        if not is_country_found:
            for country in frequent_countries:
                for info in current_location_info:
                    if country in info:
                        is_country_found = True
                        location_parts['country'] = info
                        break
                if is_country_found:
                    break
            if is_country_found:
                continue

        number = pat_num.search(location_info)

        if number or 'ул.' in location_info:
            continue

        # A számok feldolgozása, amennyiben kellenének a kimenetben

        # if number and 'этаж' not in location_info and 'кв.' not in current_location_info:
        #     is_street_num = True
        #     for poss_district in poss_districts:
        #         if poss_district in location_info:
        #             is_street_num = False
        #     if is_street_num or '№' in location_info or 'д.' in location_info or int(number.group()) > 23:
        #         location_parts['number'] = number.group()
        #     else:
        #         location_parts['district'] = number.group()
        #     continue

        current_location_type = ''
        is_county_found = False
        for poss_abbreviation_or_county_hint in current_location_info:
            for county_hint_word in county_hint_words:
                if poss_abbreviation_or_county_hint.endswith(county_hint_word):
                    location_info = poss_abbreviation_or_county_hint[: -len(county_hint_word)]
                    location_parts['county'] = location_info
                    is_county_found = True
                    break

            if is_county_found:
                break

            poss_abbreviation = poss_abbreviation_or_county_hint.lower()
            if poss_abbreviation in abbrs_rus_dict.keys():
                abbreviations_per_locaton.add(poss_abbreviation)
                abbreviations.add(poss_abbreviation)

                location_info = ' '.join([info for info in location_info.split() if info not in abbreviations_per_locaton])
                if len(current_location_type) == '':
                    current_location_type = abbrs_rus_dict[poss_abbreviation]

        if is_county_found:
            continue

        locations_per_string.append((current_location_type, abbreviations_per_locaton, location_info.strip()))

    # Ha nincsen rövidítés a sorban, de csak kettő elemből áll, akkor gyakran ország, város információt tartalmaz a sor
    if len(abbreviations) == 0 and len(locations_per_string) == 1:
        if len(location_parts['country']) > 0 and not locations_per_string[0][2].endswith('меде'):
            location_parts['city'] = locations_per_string[0][2]
            return location_parts

    scale_of_types_index = 0

    for abbreviaton in abbrs_rus_dict.keys():
        for i, (_, abb, location_info) in enumerate(locations_per_string):
            if abbreviaton in abb:
                if len(location_parts[abbrs_rus_dict[abbreviaton]]) == 0:
                    location_parts[abbrs_rus_dict[abbreviaton]] = location_info
                    del locations_per_string[i]
                else:
                    scale_of_types_index = scale_of_types.index(abbrs_rus_dict[abbreviaton]) + 1
                    if scale_of_types_index < len(scale_of_types):
                        location_parts[scale_of_types[scale_of_types_index]] = location_info
                        scale_of_types_index += 1
                        del locations_per_string[i]
                break
        if scale_of_types_index == len(scale_of_types):
            break

    # azon lokációk besorolása (ha maradt még nekik hely), amit típus (rövidítés) hiányában nem kerültek sehova
    for _, __, location_info in locations_per_string:
        if len(location_info) > 1:

            if location_info == 'Будапешт':
                temp_loc = location_parts['city']
                location_parts['city'] = location_info
                location_info = temp_loc
                if len(location_info) == 0:
                    continue

            elif location_info == 'Пешт':
                temp_loc = location_parts['county']
                location_parts['county'] = location_info
                location_info = temp_loc
                if len(location_info) == 0:
                    continue

            for i in range(len(scale_of_types)-1, -1, -1):
                if len(location_parts[scale_of_types[i]]) == 0:
                    location_parts[scale_of_types[i]] = location_info
                    break

    return location_parts


def main():
    with open('../data/Kart.csv', encoding='utf-8') as inputf:
        for line in inputf:
            string = line.strip().split('\t')
            if len(string) < 7:
                return None
            print(extract_location_parts(string[5]))
            print(extract_location_parts(string[6]))

    # # For test
    # with open('samples/out_locs.txt', 'w', encoding='utf-8') as outpf:

        # for line in sys.stdin.readlines():  # with open(sys.stdin)
        #     string = line.strip().split('\t')
        #     if len(string) < 7:
        #         return None
        #     loc_5 = extract_location_parts(string[5], row_num=string[0])
        #     if loc_5 is not None:
        #         print(loc_5, file=outpf)
        #     loc_6 = extract_location_parts(string[6], row_num=string[0])
        #     if loc_6 is not None:
        #         print(loc_6, file=outpf)


if __name__ == '__main__':
    main()
