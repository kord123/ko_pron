import json
import re
from unittest import TestCase, main
from ko_pron import romanise
from ko_pron.ko_pron import system_lookup


class TestKoPron(TestCase):
    def test_no_optional_params(self):
        for system, expected in {"ph": "한구거",
                                 "rr": "han-gugeo",
                                 "rrr": "hangug-eo",
                                 "mr": "han'gugŏ",
                                 "yr": "hankwuk.e",
                                 "ipa": "ha̠nɡuɡʌ̹"}.items():
            with self.subTest(expected=expected):
                self.assertEqual(romanise("한국어", system), expected)

    def test_long_consonant(self):
        for system, expected in {"ph": "한:구거",
                                 "rr": "han-gugeo",
                                 "rrr": "hangug-eo",
                                 "mr": "han'gugŏ",
                                 "yr": "hānkwuk.e",
                                 "ipa": "ˈha̠ːnɡuɡʌ̹"}.items():
            with self.subTest(expected=expected):
                self.assertEqual(romanise("한국어", system, l=[0]), expected)

    def test_capitalized(self):
        for system, expected in {"ph": "한구거",
                                 "rr": "Han-gugeo",
                                 "rrr": "Hangug-eo",
                                 "mr": "Han'gugŏ",
                                 "yr": "Hankwuk.e",
                                 "ipa": "ha̠nɡuɡʌ̹"}.items():
            with self.subTest(expected=expected):
                self.assertEqual(romanise("한국어", system, cap=True), expected)

    def test_compouding1(self):
        for system, expected in {"ph": "상사뼝",
                                 "rr": "sangsabyeong",
                                 "rrr": "sangsabyeong",
                                 "mr": "sangsapyŏng",
                                 "yr": "sangsaqpyeng",
                                 "ipa": "sʰa̠ŋsʰa̠p͈jʌ̹ŋ"}.items():
            result = romanise("상사병", system, com=[1])

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_compouding2(self):
        for system, expected in {"ph": "써클",
                                 "rr": "seokeul",
                                 "rrr": "seokeul",
                                 "mr": "ssŏk'ŭl",
                                 "yr": "qsekhul",
                                 "ipa": "s͈ʌ̹kxɯɭ"}.items():
            result = romanise("서클", system, com=[-1])

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_nn_and_l(self):
        for system, expected in {"ph": "의:견난",
                                 "rr": "uigyeonnan",
                                 "rrr": "uigyeonnan",
                                 "mr": "ŭigyŏnnan",
                                 "yr": "ūykyennan",
                                 "ipa": "ˈɰiːɡjʌ̹nna̠n"}.items():
            result = romanise("의견란", system, nn=[2], l=[0])

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_ui_and_l(self):
        for system, expected in {"ph": "공:산주의/공:산주이",
                                 "rr": "gongsanjuui",
                                 "rrr": "gongsanjuui",
                                 "mr": "kongsanjuŭi",
                                 "yr": "kōngsancwuuy",
                                 "ipa": "ˈko̞ːŋsʰa̠nd͡ʑuɰi] ~ [ˈko̞ːŋsʰa̠nd͡ʑui"}.items():
            result = romanise("공산주의", system, ui=3, l=[0])

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_ui_e_and_l(self):
        for system, expected in {"ph": "의/에",
                                 "rr": "ui",
                                 "rrr": "ui",
                                 "mr": "ŭi",
                                 "yr": "uy",
                                 "ipa": "ɰi] ~ [e̞"}.items():
            result = romanise("의", system, ui_e=0)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_nobc(self):
        for system, expected in {"ph": "고춛까루/고추까루",
                                 "rr": "gochutgaru",
                                 "rrr": "gochusgalu",
                                 "mr": "koch'utkaru",
                                 "yr": "kochwusqkalwu",
                                 "ipa": "ko̞t͡ɕʰut̚k͈a̠ɾu] ~ [ko̞t͡ɕʰuk͈a̠ɾu"}.items():
            result = romanise("고춧가루", system, nobc=1)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_ni(self):
        for system, expected in {"ph": "깬닙",
                                 "rr": "kkaennip",
                                 "rrr": "kkaes-ip",
                                 "mr": "kkaennip",
                                 "yr": "kkaysⁿiph",
                                 "ipa": "k͈e̞nnip̚"}.items():
            result = romanise("깻잎", system, ni=[1])

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_bcred1(self):
        for system, expected in {"ph": "가버치",
                                 "rr": "gabeochi",
                                 "rrr": "gabs-eochi",
                                 "mr": "kabŏch'i",
                                 "yr": "kaps.echi",
                                 "ipa": "ka̠bʌ̹t͡ɕʰi"}.items():
            result = romanise("값어치", system, bcred=0)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_bcred2(self):
        for system, expected in {"ph": "마틍정",
                                 "rr": "matheungjeong",
                                 "rrr": "maj-heungjeong",
                                 "mr": "mathŭngjŏng",
                                 "yr": "mac.hungceng",
                                 "ipa": "ma̠tʰɯŋd͡ʑʌ̹ŋ"}.items():
            result = romanise("맞흥정", system, bcred=0)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_svar(self):
        for system, expected in {
            "ph": "머딛따/머딛따",
            "rr": "meoditda",
            "rrr": "meos-issda",
            "mr": "mŏditta",
            "yr": "mes.issqta",
            "ipa": "mʌ̹dit̚t͈a̠] ~ [mʌ̹dit̚t͈a̠"
        }.items():
            result = romanise("멋있다", system, svar=0)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_iot(self):
        for system, expected in {
            "ph": "뛰어들다/뛰여들다",
            "rr": "ttwieodeulda",
            "rrr": "ttwieodeulda",
            "mr": "ttwiŏdŭlda",
            "yr": "ttwietulta",
            "ipa": "t͈ɥiʌ̹dɯɭda̠] ~ [t͈ɥijʌ̹dɯɭda̠] ~ [t͈yʌ̹dɯɭda̠] ~ [t͈yjʌ̹dɯɭda̠"
        }.items():
            result = romanise("뛰어들다", system, iot=1)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)

    def test_yeored(self):
        for system, expected in {
            "ph": "쳐주기다/처주기다",
            "rr": "chyeojugida",
            "rrr": "chyeojug-ida",
            "mr": "ch'yŏjugida",
            "yr": "chyecwuk.ita",
            "ipa": "t͡ɕʰjʌ̹d͡ʑuɡida̠] ~ [t͡ɕʰʌ̹d͡ʑuɡida̠"
        }.items():
            result = romanise("쳐죽이다", system, yeored=0)

            with self.subTest(result=result, expected=expected):
                self.assertEqual(result, expected)


if __name__ == '__main__':
    main()
