from app.utils.i18n import i18n
from app.utils.error import showError, window
from app.config.config import get_config
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import spacy

config = get_config()
i18n = i18n()

try:
    _spacy_model = i18n.lang_setting.get("spacy-model")
    nlp = spacy.load(_spacy_model)
except:
    showError(window, "error_spacy") #TODO: ERROR LANG

try:
    embedding_model = SentenceTransformer(config.config.embedding_model)
except:
    showError(window, "error_embedding") #TODO: ERROR LANG

try:
    emotion_model = pipeline("text-classification", model=i18n.lang_setting.get("emotion_model"))
except:
    showError(window, "error_emotion") #TODO: ERROR LANG