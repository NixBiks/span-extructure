import pytest
import spacy


@pytest.fixture(scope="module")
def nlp():
    nlp = spacy.blank("en")

    config = {
        "overwrite": False,
        "rules": [
            {
                "patterns": [[{"SHAPE": "dd.dd.dddd"}]],
                "extruct": r"(?P<day>[0-3]\d).(?P<month>0[1-9]|1[0-2]).(?P<year>20[0-5]\d|19\d\d)",
                "label": "DATE",
            }
        ],
    }
    nlp.add_pipe("span_extructure", config=config)
    return nlp


def test_span_extructure(nlp):
    doc = nlp("My birthday is 21.04.1986")
    assert len(doc.ents) == 1
    assert doc.ents[0].label_ == "DATE"
    assert doc.ents[0].text == "21.04.1986"
    assert doc.ents[0]._.extructure == {"day": "21", "month": "04", "year": "1986"}
