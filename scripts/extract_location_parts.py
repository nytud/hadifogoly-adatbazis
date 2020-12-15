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


# todo: ha kell (argumentum alapján), akkor egy típusból többet is visszaad, ha több rövidítés van
#  egy típusból


# FREQUENT_CITIES = {
#     'Арад',
#     'Берегово',
#     'Братислав',
#     'Братислава',
#     'Брно',
#     'Буда',
#     'Будапешт',
#     'Будапешта',
#     'Будапешта',
#     'Будапеште',
#     'Будапеште',
#     'Будо',
#     'Будопешт',
#     'Вишк',
#     'Иванц',
#     'Кишпешт',
#     'Клуж',
#     'Коложвар',
#     'Коломея',
#     'Кюстрин',
#     'Николаевка',
#     'Оскол',
#     'Познань',
#     'Сатумаре',
#     'Сторожевое',
#     'Ужгород',
#     'Уйпешт',
#     'Шольт'
# }
#
# FREQUENT_DISTRICTS = {
#     'Закарпатская',
#     'Закарп',
#
# }
# FREQUENT_COUNTIES = {
#     'Абауй',
#     'Бачбодрог',
#     'Бачбодрок',
#     'Берег',
#     'Боршод',
#     'Боршодь',
#     'Боршот',
#     'Ваш',
#     'Вош',
#     'Гайду',
#     'Гемер',
#     'Гойду',
#     'Земплин',
#     'Золо',
#     'Марош',
#     'Марошторда',
#     'Морош',
#     'Морошторда',
#     'Мороштордо',
#     'Обоуй',
#     'Пешт',
#     'Пешта',
#     'Саболч',
#     'Сабольч',
#     'Сабоч',
#     'Соболч',
#     'Собольч',
#     'Собоч',
#     'Угоча',
#     'Удваргей',
#     'Удворгей',
#     'Унг',
#     'Фегер',
#     'Фегир',
#     'Феер',
#     'Феир',
#     'Фехер',
#     'Хайду',
#     'Харомсек',
#     'Хойду',
#     'Шамодь',
#     'Шомодь',
#     'Шомоть',
# }

FREQUENT_COUNTRIES = [
    'Австрия',
    'Белоруссия',
    'Бессарабия',
    'Болгария',
    'Венгрия',
    'Галиция',
    'Германия',
    'Дания',
    'Латвия',
    'Польша',
    'Румыния',
    'Силезия',
    'Словакия',
    'Трансильвания',
    'Украина',
    'Чехия',
    'Чехословакия',
    'Югославия']

PAT_NUM = re.compile(r'\d+')

SCALE_OF_TYPES = ['county', 'district', 'city']  # street]

COUNTY_HINT_WORDS = {'меде', 'меди', 'медя', 'мече', 'медия'}

# Abban az esetben kikommentelendő, ha a számokat is fel szeretnénk dolgozni
# poss_districts = {'р-н', 'p-нe', 'р-он', 'р-на', 'кр.', 'к.', 'у.', 'уезд', 'у-д'}

ABBRS_RUS_DICT = {
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
    'около': 'county'  # akkor county legtöbbször, ha egyedül áll és nem egy másik rövidítéssel.
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
        for county_hint_word in COUNTY_HINT_WORDS:
            location_info = location_info.replace(f' {county_hint_word}', county_hint_word)
            location_info = location_info.replace(f'-{county_hint_word}', county_hint_word)

        location_info = location_info.strip()
        current_location_info = location_info.split()
        abbreviations_per_locaton = set()

        if not is_country_found:
            for country in FREQUENT_COUNTRIES:
                for info in current_location_info:
                    if country in info:
                        is_country_found = True
                        location_parts['country'] = info
                        break
                if is_country_found:
                    break
            if is_country_found:
                continue

        number = PAT_NUM.search(location_info)

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
        #         location_parts['district'] = number.group()  # a district járás, nem kerület. Ez a sor elhagyandó.
        #     continue

        # is_city_found = False
        # is_district_found = False
        current_location_type = ''
        is_county_found = False
        for info in current_location_info:
            for county_hint_word in COUNTY_HINT_WORDS:
                if info.endswith(county_hint_word):
                    location_info = info[: -len(county_hint_word)]
                    location_parts['county'] = location_info
                    is_county_found = True
                    break

            if is_county_found:
                break

            # is_city_found = info in FREQUENT_CITIES
            # is_county_found = info in FREQUENT_COUNTIES
            # is_district_found = info in FREQUENT_DISTRICTS
            #
            # if is_city_found:
            #     location_parts['city'] = info
            #
            # elif is_county_found:
            #     location_parts['county'] = info
            #     is_county_found = True
            #
            # elif is_district_found:
            #     location_parts['district'] = info
            #     is_district_found = True

            # if is_city_found or is_district_found or is_county_found:
            #     break

            poss_abbreviation = info.lower()

            if poss_abbreviation in ABBRS_RUS_DICT.keys():
                abbreviations_per_locaton.add(poss_abbreviation)
                abbreviations.add(poss_abbreviation)

                location_info = ' '.join([info for info in location_info.split() if info not in abbreviations_per_locaton])
                if len(current_location_type) == '':
                    current_location_type = ABBRS_RUS_DICT[poss_abbreviation]

        if is_county_found:  # is_city_found or is_district_found or is_county_found:
            continue

        locations_per_string.append((current_location_type, abbreviations_per_locaton, location_info.strip()))

    # Ha nincsen rövidítés a sorban, de csak kettő elemből áll, akkor gyakran ország, város információt tartalmaz a sor
    if len(abbreviations) == 0 and len(locations_per_string) == 1:
        if len(location_parts['country']) > 0:
            location_parts['city'] = locations_per_string[0][2]
            return location_parts

    scale_of_types_index = 0

    for abbreviaton in ABBRS_RUS_DICT.keys():
        for i, (_, abb, location_info) in enumerate(locations_per_string):
            if abbreviaton in abb:
                location_type = ABBRS_RUS_DICT[abbreviaton]
                if len(location_parts[location_type]) == 0:
                    location_parts[location_type] = location_info
                    del locations_per_string[i]
                else:
                    scale_of_types_index = SCALE_OF_TYPES.index(location_type) + 1
                    if scale_of_types_index < len(SCALE_OF_TYPES):
                        location_parts[SCALE_OF_TYPES[scale_of_types_index]] = location_info
                        scale_of_types_index += 1
                        del locations_per_string[i]
                break
        if scale_of_types_index == len(SCALE_OF_TYPES):
            break

    # azon lokációk besorolása (ha maradt még nekik hely), amit típus (rövidítés) hiányában nem kerültek sehova
    for _, __, location_info in locations_per_string:
        if len(location_info) > 1:
            for i in range(len(SCALE_OF_TYPES)-1, -1, -1):
                if len(location_parts[SCALE_OF_TYPES[i]]) == 0:
                    location_parts[SCALE_OF_TYPES[i]] = location_info
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
