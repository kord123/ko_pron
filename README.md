## Information
Hangul pronunciation and romanisation module.

This Is actally rewritten to python Wiktionary lua module  [ko-pron](https://en.wiktionary.org/wiki/Module:ko-pron)

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

## Test coverage

Name | Stmts | Miss | Cover
---- | ----- | ---- | -----
ko_pron/ko_pron/\_\_init__.py | 2 | 0 | 100%
ko_pron/ko_pron/data.py | 2 | 0 | 100%
ko_pron/ko_pron/ko_pron.py | 202 | 33 | 84%
TOTAL | 206 | 33 | 84%

## Links
Original lua module: [ko-pron](https://en.wiktionary.org/wiki/Module:ko-pron)

Optional parameters: [Parameters](https://en.wiktionary.org/wiki/Template:ko-IPA#Parameters)