import re

def mask_pii(text: str) -> str:
    """
    Redacts sensitive patterns before they reach the LLM.
    """
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, "[PRIVATE_EMAIL]", text)

    card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text = re.sub(card_pattern, "[CONFIDENTIAL_PAYMENT_INFO]", text)

    return text
