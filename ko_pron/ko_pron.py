import re
import unicodedata
from math import floor

from .data import vowels, boundary

system_lookup = ["ph", "rr", "rrr", "mr", "yr", "ipa"]
system_list = [
    {
        "seq": 1,
        "abbreviation": "ph",
        "display": "Phonetic Hangul",
        "separator": "/",
    },
    {
        "seq": 2,
        "abbreviation": "rr",
        "display": "Revised Romanization",
        "separator": "/",
    },
    {
        "seq": 3,
        "abbreviation": "rrr",
        "display": "Revised Romanization (translit.)",
        "separator": "/"
    },
    {
        "seq": 4,
        "abbreviation": "mc",
        "display": "McCune–Reischauer",
        "separator": "/"
    },
    {
        "seq": 5,
        "abbreviation": "yr",
        "display": "Yale Romanization",
        "separator": "/"
    },
    {
        "seq": 6,
        "abbreviation": "ipa",
        "display": "International Phonetic Alphabet (IPA)",
        "separator": "] ~ ["
    }
]

final_syllable_conversion = {"": "Ø", "X": ""}

com_mc = {"g": "k", "d": "t", "b": "p", "j": "ch", "sy": "s", "s": "ss"}

com_ph = {"ᄀ": "ᄁ", "ᄃ": "ᄄ", "ᄇ": "ᄈ", "ᄉ": "ᄊ", "ᄌ": "ᄍ"}

vowel_variation = {7: -56, 11: 112, 16: 0}

allowed_vowel_scheme = {"7-0": 1, "7-5": 1, "11-0": 1, "11-5": 1, "16-5": 1}

ambiguous_intersyllabic_rr = {"oe": 1, "eo": 1, "eu": 1, "ae": 1, "ui": 1}


def romanise(text_param,
             system_index,
             l: [int] = [],
             cap: bool = False,
             com: [int] = [],
             nn: [int] = [],
             ui: int = None,
             ui_e: int = None,
             nobc: int = None,
             ni: [int] = [],
             bcred: int = None,
             svar: int = None,
             iot: int = None,
             yeored: int = None):
    # system_index - One of these values:
    # "ph" - phonetic hangul
    # "rr" - Revised Romanisation
    # "rrr" - WT-revised Revised Romanisation
    # "mr" - McCune-Reischauer
    # "yr" - Yale romanisation
    # "ipa" - IPA

    system_index = system_lookup.index(system_index)
    text_param = re.sub('["-%](.)', "\\1", text_param)
    for the_original in re.finditer("[ᄀ-ᄒ" + "ᅡ-ᅵ" + "ᆨ-ᇂ" + "ㄱ-ㆎ가-힣' ]+", text_param):
        primitive_word = the_original.string

        has_vowel = {}
        for ch in primitive_word:
            jungseong = floor(((ord(ch) - 0xAC00) % 588) / 28)
            if not re.search("[예옛례롄]", ch) and re.search("[가-힣]", ch):
                has_vowel[jungseong] = True
        word_set = [primitive_word]

        if system_index in {0, 5}:
            def add_respelling(variable, modification, modification2=lambda x: x):
                if variable is not None:
                    new_word_set = []
                    for i, item in enumerate(word_set):
                        item = item[:variable] + modification(item[variable]) + \
                               modification2(item[variable + 1: variable + 2]) + item[variable + 2:]
                        new_word_set.append("".join(item))
                    word_set.extend(new_word_set)

            add_respelling(ui, lambda x: "이")
            add_respelling(ui_e, lambda x: "에")

            add_respelling(nobc, lambda x: chr(ord(x) - (ord(x) - 0xAC00) % 28), lambda x: chr(ord(x) + 588))

            add_respelling(svar, lambda x: chr(ord(x) - 12))
            add_respelling(iot, lambda x: chr(ord(x) + 56))
            add_respelling(yeored, lambda x: chr(ord(x) - 56))

        for vowel_id in {7, 11, 16}:
            if has_vowel.get(vowel_id) and "{}-{}".format(vowel_id, system_index) in allowed_vowel_scheme:
                pre_length = len(word_set)
                for i in range(0, pre_length):
                    item = word_set[i]
                    for num, it in enumerate(item):
                        if floor(((ord(it) - 0xAC00) % 588) / 28) == vowel_id:
                            item = item[:num] + chr(ord(it) + vowel_variation[vowel_id]) + item[num + 1:]
                    if vowel_id == 11:
                        word_set.insert(i, "".join(item))
                    else:
                        word_set.append("".join(item))

        word_set_romanisations = []
        for respelling in word_set:
            decomposed_syllables = decompose_syllable(respelling)
            romanisation = []
            bold_insert_count = 0
            for index in range(-1, len(decomposed_syllables)):
                this_syllable = index != -1 and respelling[index:index + 1] or ""

                syllable = index != -1 and decomposed_syllables[index] or {"initial": "Ø", "vowel": "Ø", "final": "X"}

                next_syllable = index < len(decomposed_syllables) - 1 and decomposed_syllables[index + 1] \
                                or {"initial": "Ø", "vowel": "Ø", "final": "Ø"}

                if syllable['final'] in final_syllable_conversion:
                    syllable['final'] = final_syllable_conversion[syllable['final']]

                if system_index == 4 and syllable['vowel'] == "ᅮ" and match(syllable['initial'], "[ᄆᄇᄈᄑ]"):
                    syllable['vowel'] = "ᅳ"

                if system_index in {0, 5}:
                    if syllable['vowel'] == "ᅴ" and this_syllable != "의":
                        syllable['vowel'] = "ᅵ"
                    if this_syllable == "넓":
                        if match(next_syllable['initial'], "[ᄌᄉ]"):
                            syllable['final'] = "ᆸ"
                        elif next_syllable['initial'] == "ᄃ":
                            if match(next_syllable['vowel'], "[^ᅡᅵ]"):
                                syllable['final'] = "ᆸ"

                vowel = vowels[syllable['vowel']][system_index]

                if index + 1 in nn:
                    next_syllable['initial'] = "ᄂ"
                if index in com and system_index in {0, 5}:
                    next_initial = next_syllable['initial']
                    next_syllable['initial'] = com_ph[next_initial] if next_initial in com_ph else next_initial

                if index + 1 in ni and system_index != 2:
                    next_syllable['initial'] = (system_index == 4 and syllable['final'] == "ᆯ") and "ᄅ" or "ᄂ"

                if system_index not in {2, 4}:
                    if bcred == index:
                        syllable['final'] = boundary[syllable['final'] + "-Ø"][0]

                    if index != -1 and this_syllable == "밟":
                        syllable['final'] = "ᆸ"

                    final_next_syllable = syllable['final'] + respelling[index + 1: index + 2]
                    if match(final_next_syllable, "[ᇀᆴ][이히]"):
                        syllable['final'] = "ᆾ"

                    elif match(final_next_syllable, "ᆮ이"):
                        syllable['final'] = "ᆽ"

                    elif match(final_next_syllable, "ᆮ히"):
                        syllable['final'] = "ᆾ"

                bound = "{}-{}".format(syllable['final'], next_syllable['initial'])
                if bound not in boundary:
                    raise ValueError("No boundary data for " + bound + ".")

                junction = boundary[bound][system_index]

                if index in l:
                    if system_index == 0:
                        def substitute(matched):
                            a, b = matched.group(1), matched.group(2)
                            return match(a, "[ᆨ-ᇂ]") and a + ":" + b or ":" + a + b

                        junction = gsub(junction, "^(.)(.?)$", substitute)

                    elif system_index == 4:
                        vowel = gsub(vowel, "([aeiou])", "\\1̄")

                    elif system_index == 5:
                        vowel = vowel + "ː"

                if 0 in l and index == -1 and system_index == 5 and len(decomposed_syllables) > 1:
                    vowel = vowel + "ˈ"

                if index in com:
                    def substitute(next_letter):
                        letter_val = next_letter.group()
                        return (system_index == 4 and "q" or "") \
                               + (system_index == 3
                                  and (com_mc.get(letter_val + (cap and 1 or "")) or
                                       com_mc.get(letter_val)
                                       or letter_val) or letter_val)

                    junction = gsub(junction, "(.)$", substitute)

                if index + 1 in ni and system_index == 4:
                    junction = gsub(junction, "n$", "ⁿ")
                    junction = gsub(junction, "l$", "ˡ")

                romanisation.append(vowel + junction)

            temp_romanisation = "".join(romanisation)
            if cap and system_index not in {0, 5}:
                temp_romanisation = temp_romanisation[0].upper() + temp_romanisation[1:]

            if system_index == 0:
                temp_romanisation = tidy_phonetic(primitive_word, unicodedata.normalize('NFC', temp_romanisation))
            elif system_index in {1, 2}:
                for i in range(0, 2):
                    def substitute(matched):
                        a, b = matched.group(1), matched.group(2)
                        return a + (ambiguous_intersyllabic_rr.get(a + b) and "-" or "") + b

                    temp_romanisation = gsub(temp_romanisation, "(.)…(.)", substitute)
            elif system_index == 3:
                temp_romanisation = gsub(temp_romanisation, "swi", "shwi")
            word_set_romanisations.append(temp_romanisation)

        text_param = gsub(
            text_param,
            primitive_word,
            system_list[system_index]['separator'].join(word_set_romanisations),
            1
        )
        if system_index == 5:
            text_param = tidy_ipa(text_param)
    return text_param


def decompose_syllable(word: str):
    return [decompose_jamo(syllable) for syllable in word]


def tidy_phonetic(original: str, romanised: str):
    j, k, w = 0, 0, []
    for i in range(0, len(romanised)):
        romanised_syllable = romanised[k:k + 1]
        original_syllable = original[j:j + 1]

        w += romanised_syllable
        if romanised_syllable != original_syllable:
            if match(original_syllable, "[^: ]"):
                k = k + 1
            if match(romanised_syllable, "[^: ]"):
                j = j + 1
        else:
            j, k = j + 1, k + 1
    return "".join(w)


def tidy_ipa(ipa: str):
    ipa = re.sub("ʌ̹ː", "ɘː", ipa)
    ipa = re.sub("ɭɭ([ji])", "ɭʎ\\1", ipa)
    ipa = re.sub("s([͈]?)ʰɥi", "ʃ\\1ʰɥi", ipa)
    ipa = re.sub("s([ʰ͈])([ji])", "ɕ\\1\\2", ipa)
    ipa = re.sub("nj", "ɲj", ipa)

    for key, value in {
        "kʰi": "kçi",
        "kʰj": "kçj",
        "kʰɯ": "kxɯ"
    }.items():
        ipa = ipa.replace(key, value)

    for key, value in {
        "hi": "çi",
        "hj": "çj",
        "hɯ": "xɯ",
        "ho": "ɸʷo",
        "hu": "ɸʷu",
        "hw": "ɸw",
        "ɦi": "ʝi",
        "ɦj": "ʝj",
        "ɦɯ": "ɣɯ",
        "ɦo": "βo",
        "ɦu": "βu",
        "ɦw": "βw"
    }.items():
        ipa = ipa.replace(key, value)

    if match(ipa, "ɥi"):
        midpoint = floor(len(ipa) / 2)
        ipa = ipa[0:midpoint] + ipa[midpoint:].replace("ɥi", "y")
    return ipa


def gsub(string, pattern, replacement, count=0):
    return re.sub(pattern, replacement, string, count)


def match(string, regex):
    return re.search(regex, string)


def decompose_jamo(syllable):
    if not match(syllable, "[가-힣]"):
        if match(syllable, "[ᄀ-ᄒ]"):
            return {'initial': syllable, 'vowel': "Ø", 'final': "Ø"}
        elif match(syllable, "[ᅡ-ᅵ]"):
            return {'initial': "Ø", 'vowel': syllable, 'final': "Ø"}
        elif match(syllable, "[ᆨ-ᇂ]"):
            return {'initial': "Ø", 'vowel': "Ø", 'final': syllable}
        elif match(syllable, "[ㄱ-ㆎ]"):
            return {'initial': "Ø", 'vowel': "Ø", 'final': syllable}
        else:
            return {'initial': "Ø", 'vowel': " ", 'final': "X"}

    cp = ord(syllable)
    if not cp:
        return {"", "", ""}
    relative_cp = cp - 0xAC00
    jongseong = relative_cp % 28
    jungseong = floor((relative_cp % 588) / 28)
    choseong = floor(relative_cp / 588)
    choseong, jungseong, jongseong = chr(0x1100 + choseong), chr(0x1161 + jungseong), \
                                     jongseong != 0 and chr(0x11A7 + jongseong) or ""
    return {'initial': choseong, 'vowel': jungseong, 'final': jongseong}
