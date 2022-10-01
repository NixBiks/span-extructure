import dataclasses
import re
import typing as t

import spacy
import spacy.tokens
from spacy.language import Language
from spacy.pipeline.span_ruler import PatternType, SpanRuler

DateFormat = str
SinglePattern = str | list[dict[str, t.Any]]


@dataclasses.dataclass
class Rule:
    patterns: list[SinglePattern]
    extruct: str
    label: str


@dataclasses.dataclass
class CompiledRule(Rule):
    compiled_extruct: re.Pattern


@Language.factory("span_extructure", default_config={"rules": [], "overwrite": False})
def make_span_extructure(nlp, name, rules: list[Rule], overwrite: bool):
    return SpanExtructure(nlp=nlp, name=name, rules=rules, overwrite=overwrite)


class SpanExtructure:
    def __init__(self, nlp, *, name: str, rules: list[Rule], overwrite: bool):
        self.nlp = nlp
        self.name = name
        self.ruler = SpanRuler(
            nlp, annotate_ents=True, validate=True, overwrite=overwrite
        )
        spacy.tokens.Span.set_extension("extructure", default={})
        self.rules_by_id: dict[str, CompiledRule] = {
            rule.extruct: CompiledRule(
                patterns=rule.patterns,
                extruct=rule.extruct,
                compiled_extruct=re.compile(rule.extruct),
                label=rule.label,
            )
            for rule in rules
        }

        for rule_id, rule in self.rules_by_id.items():
            self.ruler.add_patterns(
                [
                    {"label": rule.label, "pattern": p, "id": rule_id}
                    for p in rule.patterns
                ]
            )

    def __call__(self, doc):
        matches = self.ruler.match(doc)
        for span in matches:
            extruct = self.rules_by_id[span.id_].compiled_extruct
            re_matches = extruct.match(span.text)
            if not re_matches:
                continue
            span._.extructure = re_matches.groupdict()

        self.ruler.set_annotations(doc, matches)
        return doc
