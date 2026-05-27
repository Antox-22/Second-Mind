from app.utils.i18n import i18n as I18N
from app.utils.error import showError, window
from app.config.config import get_config
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import spacy

config = get_config()
_i18n = I18N()

nlp = None
embedding_model = None
emotion_model = None

# SPACY
try:
    spacy_model_name = _i18n.lang_setting.get("spacy-model")
    nlp = spacy.load(spacy_model_name)
except Exception:
    showError(window, "error_spacy")

# EMBEDDING MODEL
try:
    embedding_model = SentenceTransformer(config.config.embedding_model)
except Exception:
    showError(window, "error_embedding")

# EMOTION MODEL
try:
    model_name = _i18n.lang_setting.get("emotion_model")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=False
    )

    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    emotion_model = pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        truncation=True
    )
except Exception:
    showError(window, "error_emotion")