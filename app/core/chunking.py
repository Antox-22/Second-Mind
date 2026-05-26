from app.utils.i18n import i18n
from app.utils.error import showError
import numpy as np
import spacy

_spacy_model = i18n().lang_setting.get("spacy-model")
nlp = spacy.load(_spacy_model)

def split_sentences(text: str) -> list[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

