import re
from bs4 import BeautifulSoup

def check_su_note_content(su_note_content):
    """
    Vérifier si tous les mots-clés sont présents dans le contenu de su_note.
    Args:
        su_note_content (str): Contenu de la colonne su_note.
    Returns:
        bool: True si tous les mots-clés sont présents, False sinon.
    """
    # List of keywords to check for
    keywords_to_check = [
        "@gmail.com",
        "Podsumowanie zawodowe"
    ]
    # Load the content into BeautifulSoup for parsing
    soup = BeautifulSoup(su_note_content, 'html.parser')
    # Check if all keywords are present in the content
    for keyword in keywords_to_check:
        if keyword not in soup.get_text():
            return None
    
    return su_note_content

def divide_elements(s: str, replace_su_note=True, min_word_count=75):
    """CHECK LENGHT

    Args:
        s (str): _description_
        replace_su_note (bool, optional): _description_. Defaults to True.
        min_word_count (int, optional): _description_. Defaults to 75.

    Returns:
        _type_: _description_
    """
    pattern = r'(\[su_note note_color="#fafafa" text_color="#233143"\](.*?)\[\/su_note\])'
    match = re.search(pattern, s, flags=re.DOTALL)  # re.DOTALL ensures that . matches newline characters as well

    su_note = match.group(1) if match else None
    if su_note:
        word_count = re.findall(r'\b\w+\b', su_note)
        print(word_count)
        if len(word_count) <= min_word_count:
            su_note = None
        # if not check_su_note_content():
        #     su_note = None

    if replace_su_note:
        s = re.sub(pattern, '', s, count=1, flags=re.DOTALL)

    return str(s), str(su_note)


def extractH2(centent:str):
    """EXTRACT H2 TAG

    Args:
        centent (str): _description_

    Returns:
        _type_: _description_
    """
    soup = BeautifulSoup(centent, 'html.parser')
    first_h2 = soup.find('h2')
    first_h2, _ = divide_elements(s=str(first_h2))
    return first_h2


