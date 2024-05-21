from transformers import pipeline

classifier = pipeline("text-classification", model="unitary/toxic-bert")


def check_toxicity(text, threshold=0.5):
    """
    Checks the toxicity of a given text.

    Parameters:
    - text (str): The text to check for toxicity.
    - threshold (float): The threshold score for considering a text as toxic. Default is 0.5.

    Returns:
    - bool: True if the text is toxic and its score is above the threshold, False otherwise.
    """
    results = classifier(text)
    for result in results:
        if result["label"] == "toxic" and result["score"] >= threshold:
            return True
    return False
