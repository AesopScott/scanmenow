"""spaCy NER wrapper — named entity recognition for PII/PHI detection."""

import time
import logging
from typing import List, Tuple

import spacy
from spacy.language import Language

logger = logging.getLogger(__name__)

_NLP_CACHE: Language | None = None
DEFAULT_MODEL = "en_core_web_lg"


def get_nlp(model: str = DEFAULT_MODEL) -> Language:
    """
    Load and return the spaCy NLP model, caching after first load.

    Args:
        model: spaCy model name (default: 'en_core_web_lg').

    Returns:
        Loaded spaCy Language model.
    """
    global _NLP_CACHE
    if _NLP_CACHE is None:
        start = time.perf_counter()
        _NLP_CACHE = spacy.load(model)
        elapsed = time.perf_counter() - start
        logger.info("spaCy model '%s' loaded in %.2fs", model, elapsed)
    return _NLP_CACHE


def extract_entities(text: str) -> List[Tuple[str, str, int, int]]:
    """
    Extract named entities from text using spaCy NER.

    Args:
        text: Input text to process.

    Returns:
        List of (text, label, start_char, end_char) tuples.
    """
    nlp = get_nlp()
    doc = nlp(text)
    return [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]
