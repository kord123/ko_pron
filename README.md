## Information
Hangul pronunciation and romanisation module.

This is actally rewritten to python Wiktionary lua module  [ko-pron](https://en.wiktionary.org/wiki/Module:ko-pron)
Current revision: https://en.wiktionary.org/w/index.php?title=Module_talk:ko-pron&oldid=49615051

Supported transformations:
* Revised Romanisation (rr)
* phonetic hangul (ph)
* Yale romanisation (yr)
* McCune-Reischauer (mr)
* WT-revised Revised Romanisation (rrr)
* IPA (ipa)

McCune-Reischauer, IPA, Revised Romanisation, phonetic hangul take into aacount changes in pronunciation like:
"있다" is pronounced as "itta" etc.

Method "romanise" also accepts optional parameters. They are described in [documentation of original lua module](https://en.wiktionary.org/wiki/Template:ko-IPA#Parameters)
## Usage

```python 
from ko_pron import romanise

print(romanise("있다", "mr"))
```
Result: `itta`

## Install locally
```bash
pip install -e .
```

## Test coverage
Run tests with coverage
```bash
cd test
./coverage.sh
```
Run html tests after running tests
```bash
coverage html
```

Results

Name | Stmts | Miss | Cover
---- | ----- | ---- | -----
/Users/andrey/Projects/ko_pron/ko_pron/\_\_init__.py | 2 | 0|100%
/Users/andrey/Projects/ko_pron/ko_pron/data.py|2|0|100%
/Users/andrey/Projects/ko_pron/ko_pron/ko_pron.py|186|23|88%
test_params.py|77|0|100%
test_pronunciation.py|11|0|100%
----------------------------------------------------- | -----| -----| -----
TOTAL|278|23|92%


## Links

[GitHub](https://github.com/kord123/ko_pron)

[Original lua module](https://en.wiktionary.org/wiki/Module:ko-pron)

[Optional parameters](https://en.wiktionary.org/wiki/Template:ko-IPA#Parameters)