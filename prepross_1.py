import re


def divide_elements(s: str, replace_su_note=True, min_word_count=75):
    pattern = r'(\[su_note note_color="#fafafa" text_color="#233143"\](.*?)\[\/su_note\])'
    match = re.search(pattern, s, flags=re.DOTALL)  # re.DOTALL ensures that . matches newline characters as well

    su_note = match.group(1) if match else None
    if su_note:
        # Count words in su_note content
        word_count = re.findall(r'\b\w+\b', su_note)
        if word_count <= min_word_count:
            su_note = None

    if replace_su_note:
        s = re.sub(pattern, '', s, count=1, flags=re.DOTALL)

    return str(s), str(su_note)


def extractH2(centent:str):
    motif = r'<h2>(.*?)<\/h2>'
    return re.findall(motif, centent, re.DOTALL)

def createTitleColumn(reader_csv):
    for ligne in reader_csv:
        # Utiliser regex pour extraire le contenu de <h2> de la colonne "Content"
        content = ligne['Content']
        resultat_regex = extractH2(content)
        if resultat_regex:
            titre = resultat_regex.group(1)
        else:
            titre = ''  # Si <h2> n'est pas trouvé, laisser la valeur vide

        # Ajouter la nouvelle valeur à la ligne
        ligne['Letter Tittle'] = titre
        ligne['Letter'] = divide_elements(s=content)
