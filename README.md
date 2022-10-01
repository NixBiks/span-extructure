# Span Extructure

[![codecov](https://codecov.io/gh/mr-bjerre/span-extructure/branch/main/graph/badge.svg?token=MSMW9LZLA0)](https://codecov.io/gh/mr-bjerre/span-extructure)

You might think the name is mispelled but it ain't. It is a word play on [spaCy's](https://spacy.io/) `Span`, _extract_ and _structure_. `span_exctructure` is a spaCy component that builds upon `SpanRuler` and regex to extract structured information, e.g. dates, amounts with currency and multipliers etc.

## Installation

```
pip install span_extructure
```

## Usage

```py
import spacy

nlp = spacy.blank("en")

# Optionally add config if varying from default values
config = {
    "overwrite": False,       # default: False
    "rules": [
        {
            "patterns": [[{"SHAPE": "dd.dd.dddd"}]],
            "extruct": r"(?P<day>[0-3]\d).(?P<month>0[1-9]|1[0-2]).(?P<year>20[0-5]\d|19\d\d)",
            "label": "DATE",
        }
    ]
}
nlp.add_pipe("span_extructure", config=config)

doc = nlp("This date 21.04.1986 will be a DATE entity while the structured information will be extracted to `Span._.extructure`")
for e in doc.ents:
    print(f"{e.text}\t{e.label_}\t{e._.extructure}")
```

```bash
>>> 21.04.1986      DATE    {'day': '21', 'month': '04', 'year': '1986'}
```
