from django.conf import settings
from transformers import pipeline

classifier = None

if settings.USE_AI_MODELS:
    classifier = pipeline("text-classification", model="unitary/toxic-bert")


def chunk_text(text, chunk_size=512):
    """
    Splits the input text into chunks of a specified size.

    Parameters:
    - text (str): The text to be split.
    - chunk_size (int): The size of each chunk. Default is 512.

    Returns:
    - list: A list of text chunks.
    """
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def check_toxicity(text, threshold=0.5):
    """
    Checks the toxicity of a given text by splitting it into chunks and analyzing each chunk.

    Parameters:
    - text (str): The text to check for toxicity.
    - threshold (float): The threshold score for considering a text as toxic. Default is 0.5.

    Returns:
    - bool: True if any chunk of the text is toxic and its score is above the threshold, False otherwise.
    """
    if not settings.USE_AI_MODELS:
        return False

    chunks = chunk_text(text)
    for chunk in chunks:
        results = classifier(chunk)
        for result in results:
            if result["label"] == "toxic" and result["score"] >= threshold:
                return True
    return False
