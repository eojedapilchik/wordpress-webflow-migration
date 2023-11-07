from bs4 import BeautifulSoup

"""
    THE INPUT OF EACH FUNCTION IS THE HTML (IN THE CONTENT COLUMN)
    THE OUTPUT IS THE HTML MODIFIED
"""

def change_class(html:str) -> str:
    """_summary_

    Args:
        html (str): _description_

    Returns:
        str: _description_
    """
    soup = BeautifulSoup(html, 'html.parser')

    first_span_to_replace = soup.find('span', {'data-color': 'var(--green-10)'})

    if first_span_to_replace:
        new_element = soup.new_tag('p')
        new_element.string = first_span_to_replace.get_text()
        first_span_to_replace.replace_with(new_element)

    other_spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in other_spans_to_remove[1:]:
        span.extract()
    modified_html:str = soup.prettify()
    return modified_html

def del_span(html:str) -> str:
    html = change_class(html)
    soup = BeautifulSoup(html, 'html.parser')
    spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in spans_to_remove:
        span.unwrap()

    modified_html:str = soup.prettify()
    return modified_html

def del_i_in_li(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li')

    for li in li_elements:
        i_elements = li.find_all('i')
        for i in i_elements:
            i.extract()

    modified_html = soup.prettify()
    modified_html = str(modified_html).replace(':white_check_mark:', '').replace(':x:', '')
    return modified_html

def change_class(html:str) -> str:
    """_summary_

    Args:
        html (str): _description_

    Returns:
        str: _description_
    """
    soup = BeautifulSoup(html, 'html.parser')

    first_span_to_replace = soup.find('span', {'data-color': 'var(--green-10)'})

    if first_span_to_replace:
        new_element = soup.new_tag('p')
        new_element.string = first_span_to_replace.get_text()
        first_span_to_replace.replace_with(new_element)

    other_spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in other_spans_to_remove[1:]:
        span.extract()
    modified_html:str = soup.prettify()
    return modified_html

def del_span(html:str) -> str:
    html = change_class(html)
    soup = BeautifulSoup(html, 'html.parser')
    spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in spans_to_remove:
        span.unwrap()

    modified_html:str = soup.prettify()
    return modified_html

def del_i_in_li(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li')

    for li in li_elements:
        i_elements = li.find_all('i')
        for i in i_elements:
            i.extract()

    modified_html = soup.prettify()
    modified_html = str(modified_html).replace(':white_check_mark:', '').replace(':x:', '')
    return modified_html

def change_class(html:str) -> str:
    """_summary_

    Args:
        html (str): _description_

    Returns:
        str: _description_
    """
    soup = BeautifulSoup(html, 'html.parser')

    first_span_to_replace = soup.find('span', {'data-color': 'var(--green-10)'})

    if first_span_to_replace:
        new_element = soup.new_tag('p')
        new_element.string = first_span_to_replace.get_text()
        first_span_to_replace.replace_with(new_element)

    other_spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in other_spans_to_remove[1:]:
        span.extract()
    modified_html:str = soup.prettify()
    return modified_html

def del_span(html:str) -> str:
    html = change_class(html)
    soup = BeautifulSoup(html, 'html.parser')
    spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in spans_to_remove:
        span.unwrap()

    modified_html:str = soup.prettify()
    return modified_html

def del_i_in_li(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li')

    for li in li_elements:
        i_elements = li.find_all('i')
        for i in i_elements:
            i.extract()

    modified_html = soup.prettify()
    modified_html = str(modified_html).replace(':white_check_mark:', '').replace(':x:', '')
    return modified_html

def change_class(html:str) -> str:
    """_summary_

    Args:
        html (str): _description_

    Returns:
        str: _description_
    """
    soup = BeautifulSoup(html, 'html.parser')

    first_span_to_replace = soup.find('span', {'data-color': 'var(--green-10)'})

    if first_span_to_replace:
        new_element = soup.new_tag('p')
        new_element.string = first_span_to_replace.get_text()
        first_span_to_replace.replace_with(new_element)

    other_spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in other_spans_to_remove[1:]:
        span.extract()
    modified_html:str = soup.prettify()
    return modified_html

def del_span(html:str) -> str:
    html = change_class(html)
    soup = BeautifulSoup(html, 'html.parser')
    spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in spans_to_remove:
        span.unwrap()

    modified_html:str = soup.prettify()
    return modified_html

def del_i_in_li(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li')

    for li in li_elements:
        i_elements = li.find_all('i')
        for i in i_elements:
            i.extract()

    modified_html = soup.prettify()
    modified_html = str(modified_html).replace(':white_check_mark:', '').replace(':x:', '')
    return modified_html

def change_class(html:str) -> str:
    """_summary_

    Args:
        html (str): _description_

    Returns:
        str: _description_
    """
    soup = BeautifulSoup(html, 'html.parser')

    first_span_to_replace = soup.find('span', {'data-color': 'var(--green-10)'})

    if first_span_to_replace:
        new_element = soup.new_tag('p')
        new_element.string = first_span_to_replace.get_text()
        first_span_to_replace.replace_with(new_element)

    other_spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in other_spans_to_remove[1:]:
        span.extract()
    modified_html:str = soup.prettify()
    return modified_html

def del_span(html:str) -> str:
    html = change_class(html)
    soup = BeautifulSoup(html, 'html.parser')
    spans_to_remove = soup.find_all('span', {'data-color': 'var(--green-10)'})
    for span in spans_to_remove:
        span.unwrap()

    modified_html:str = soup.prettify()
    return modified_html

def del_i_in_li(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    li_elements = soup.find_all('li')

    for li in li_elements:
        i_elements = li.find_all('i')
        for i in i_elements:
            i.extract()

    modified_html = soup.prettify()
    modified_html = str(modified_html).replace(':white_check_mark:', '').replace(':x:', '')
    return modified_html
