import csv
import os
import requests
import re
import datetime
from bs4 import BeautifulSoup


def wrap_with_p_tags(content: str) -> str:
    lines = content.strip().split("\n")
    wrapped_lines = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if not stripped_line.startswith(('<', '[')):
            wrapped_lines.append(f"<p>{stripped_line}</p>")
        else:
            wrapped_lines.append(stripped_line)

    # Join back into a single string
    return '\n'.join(wrapped_lines)


def clean_images_alt_text(text):
    # Remove consecutive pipes with no text in between
    return '|'.join([s for s in text.split('|') if s.strip()])


def extract_first_image_url(image_url_field):
    # Split by '%7C%7C' and take the first URL
    return image_url_field.split('||')[0]


def fetch_html(permalink):
    try:
        result = {}
        response = requests.get(permalink)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        target_div = soup.find('div', class_="et_pb_section et_pb_section_1_tb_body et_section_regular")

        # Fetch the title tag content
        title_tag = soup.head.find('title')
        title_content = title_tag.string if title_tag else None

        # Fetch the meta description content
        description_tag = soup.head.find('meta', attrs={"name": "description"})
        description_content = description_tag['content'] if description_tag else None

        if target_div:
            su_note_div = target_div.find('div', class_='su-note')
            su_note_content = str(su_note_div) if su_note_div else None
            if su_note_content:
                su_note_div.decompose()
                result["su_note"] = clean_elements(su_note_content)

        result["title"] = title_content
        result["description"] = description_content
        if target_div:
            result["content"] = str(target_div)

        return result
    except requests.RequestException:
        print(f"[-] Failed to fetch HTML content for {permalink}")
        return None


def divide_elements(s: str, replace_su_note=True):
    pattern = r'(\[su_note note_color="#fafafa" text_color="#233143"\](.*?)\[\/su_note\])'
    match = re.search(pattern, s, flags=re.DOTALL)  # re.DOTALL ensures that . matches newline characters as well

    su_note = match.group(1) if match else None
    if replace_su_note:
        s = re.sub(pattern, '', s, count=1, flags=re.DOTALL)

    return str(s), str(su_note)


def clean_elements(s: str) -> str:
    if not s:
        return ""
    pattern = r'\[su_([a-z]+)(?:[^\]]+)?\]'
    cleaned = re.sub(pattern, '', s)
    cleaned = (cleaned.replace('[/su_note]', '').replace('[/su_list]', '')
               .replace('[/su_box]', '').replace('[/su_highlight]', ''))
    return cleaned


def remove_span_colors(s: str) -> str:
    if not s:
        return ""

    # Regex pattern to match <span data-color="...."> and its closing tag </span>
    pattern = r'<span data-color="[^"]*">(.*?)</span>'

    # Replace matched tags with the content inside them
    cleaned = re.sub(pattern, r'\1', s)

    return cleaned


def convert_br_tags(s: str) -> str:
    return s.replace('</br>', '<br>')


def add_attribute(s: str) -> str:
    # Pattern to match <h2> and <ul> tags
    pattern_h2 = r'<h2>'
    pattern_ul = r'<ul>'

    # Add class="mb-24" to <h2> and <ul> tags
    s = re.sub(pattern_h2, r'<h2 class="mb-24">', s)
    s = re.sub(pattern_ul, r'<ul class="mb-24">', s)

    return s


def fix_div_tags(s: str) -> str:
    # Pattern to match <div> tags
    cleaned = s.replace('</div></div><br></p>', '</p></div>\n</div><br>')
    cleaned = cleaned.replace('</div><br></p>', '</p></div>\n</div>')
    return cleaned


def transform_su_box(match):
    color_class_map = {
        "#3be863": [
            "green",
            "https://assets.website-files.com/639975e5f44de65498a14a0e/63a0b5fcd66a3b979be8565b_icon-check.svg",
        ],
        "#ff826f": [
            "red",
            "https://assets.website-files.com/639975e5f44de65498a14a0e/63a0b5fcd66a3bca63e8565c_Group.svg",
        ],
    }
    title = match.group(1)
    color = match.group(2)
    content = match.group(3).strip()
    color_class = color_class_map.get(color, "blue")

    content = re.sub(r'<p>', '<p class="lh-2">', content)

    return (f'<div class="{color_class[0]}-highlight">'
            f'<div class="{color_class[0]}-highlight-cont"><img src='
            f'\'{color_class[1]}\'>'
            f'{title}'
            f'</div>'
            f'<div>{content}</div></div><br>')


def transform_su_note(match):
    color = match.group(1)
    content = match.group(2).strip()
    if color == "#fafafa":
        return f'<div class="grey-div">\n{content}\n</div><br>'
    return f'<div class="blue-highlight">\n<div class="blue-highlight-flex">\n<div>{content}</div>\n</div>\n</div><br>'


def remove_images(text):
    img_pattern = r'<img class="alignnone size-full wp-image-\d+"[^>]*>'
    text_without_images = re.sub(img_pattern, '', text)

    return text_without_images


def replace_images_with_attributes(text, new_attributes):
    img_pattern = r'<img[^>]*>'
    text_with_replaced_images = re.sub(img_pattern, lambda match: replace_image(match.group(0), new_attributes), text)
    return text_with_replaced_images


def replace_image(img_tag, new_attributes):
    exclude_src = [
        "https://assets.website-files.com/639975e5f44de65498a14a0e/63a0b5fcd66a3bca63e8565c_Group.svg",
        "https://assets.website-files.com/639975e5f44de65498a14a0e/63a0b5fcd66a3b979be8565b_icon-check.svg",
    ]
    src_match = re.search(r'src="([^"]+)"', img_tag)
    if src_match:
        src = src_match.group(1)
        if src in exclude_src:
            return img_tag
        # Replace or add width and height attributes
        if re.search(r'(width|height)="[^"]*"', img_tag):
            img_tag = re.sub(r'(width|height)="[^"]*"', new_attributes, img_tag)
        else:
            img_tag = img_tag.replace('<img', f'<img {new_attributes}')

    return img_tag


def replace_elements(input_string):
    # Pattern for [su_box]
    box_pattern = r'\[su_box title="(.*?)" box_color="(.*?)"\](.*?)\[/su_box\]'
    input_string = re.sub(box_pattern, transform_su_box, input_string, flags=re.DOTALL)

    # Pattern for [su_note]
    note_pattern = r'\[su_note note_color="(.*?)" text_color=["“]#233143[”"]\](.*?)\[/su_note\]'
    input_string = re.sub(note_pattern, transform_su_note, input_string, flags=re.DOTALL)

    return input_string


def process_rows(input_path):
    titles_to_skip = [
        "Wzory życiorysów dla analityka biznesowego",
        "Życiorysy dla fotografów",
        "Przykłady życiorysów dla menedżera ds. marketingu"
    ]

    titles_to_include = [
    ]

    titles_to_skip = [title.lower() for title in titles_to_skip]
    with (open(input_path, 'r', encoding='utf-8') as csv_file):
        reader = csv.reader(csv_file)
        headers = next(reader)
        if 'content_html' not in headers:
            headers.append('meta Title')
            headers.append('meta Description')
            headers.append('su_note')
            # headers.append('su_note2')
            # headers.append('content_html')

        yield headers  # Yield headers first

        for row in reader:
            title = row[2]
            category = row[10]
            if title.lower() in titles_to_skip:
                print(f"Skipping ${title}")
                continue

            if titles_to_include and len(titles_to_include) > 0:
                if title not in titles_to_include:
                    print(f"Skipping ${title}")
                    continue

            content_idx = headers.index("Content")
            wrapped_content = wrap_with_p_tags(row[content_idx])
            content = remove_span_colors(wrapped_content)
            content = convert_br_tags(content)
            content = add_attribute(content)
            replace = category != "Poszukiwanie pracy"
            content, su_note = divide_elements(content, replace)
            content = fix_div_tags(clean_elements(replace_elements(content)))
            content = remove_images(content)
            content = replace_images_with_attributes(content, 'width="700" height="auto"')
            su_note = clean_elements(replace_elements(su_note))

            row[content_idx] = content

            alt_text_idx = headers.index("Images Alt Text")
            row[alt_text_idx] = clean_images_alt_text(row[alt_text_idx])

            image_url_idx = headers.index("Image URL")
            row[image_url_idx] = extract_first_image_url(row[image_url_idx])

            permalink_idx = headers.index("Permalink")
            html_response = fetch_html(row[permalink_idx])

            meta_title = html_response["title"] if html_response else None
            meta_description = html_response["description"] if html_response else None

            # content_html = html_response.get("content", "") if html_response else None

            su_note2 = html_response.get("su_note", "") if html_response else None

            row.append(meta_title)
            row.append(meta_description)
            row.append(su_note)
            # row.append(su_note2)
            # row.append(content_html)
            yield row


def process_csv(input_path, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as out_csv_file:
        writer = csv.writer(out_csv_file)
        index = 0
        for row in process_rows(input_path):
            writer.writerow(row)
            print(f"Processed row {index}")
            index += 1


def process_csv_batch(input_path, output_folder):
    base_name = os.path.basename(input_path).replace(".csv", "")

    file_count_pracy = 1
    file_count_cv = 1
    row_count_pracy = 0
    row_count_cv = 0

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    out_csv_file_pracy = open(os.path.join(output_folder, f"{timestamp}_pracy_processed_{file_count_pracy}.csv"),
                              'w', newline='', encoding='utf-8')
    out_csv_file_cv = open(os.path.join(output_folder, f"{timestamp}_cv_processed_{file_count_cv}.csv"), 'w',
                           newline='', encoding='utf-8')
    writer_pracy = csv.writer(out_csv_file_pracy)
    writer_cv = csv.writer(out_csv_file_cv)

    for row in process_rows(input_path):  # Iterating over the generator
        category = row[10] if len(row) > 10 else None

        if category == "Poszukiwanie pracy":
            writer = writer_pracy
            row_count = row_count_pracy
            out_csv_file = out_csv_file_pracy
        else:
            writer = writer_cv
            row_count = row_count_cv
            out_csv_file = out_csv_file_cv

        if row_count == 0:  # if it's the header
            writer.writerow(row)
        else:
            if row_count % 50 == 0:  # For every 100 rows, switch the output file
                out_csv_file.close()
                if category == "Poszukiwanie pracy":
                    file_count_pracy += 1
                    out_csv_file_pracy = open(
                        os.path.join(output_folder, f"{timestamp}_pracy_processed_{file_count_pracy}.csv"), 'w',
                        newline='', encoding='utf-8')
                    writer_pracy = csv.writer(out_csv_file_pracy)
                    writer_pracy.writerow(next(process_rows(input_path)))  # Write headers to the new file
                    writer = writer_pracy
                else:
                    file_count_cv += 1
                    out_csv_file_cv = open(os.path.join(output_folder, f"{timestamp}_cv_processed_{file_count_cv}.csv"),
                                           'w', newline='', encoding='utf-8')
                    writer_cv = csv.writer(out_csv_file_cv)
                    writer_cv.writerow(next(process_rows(input_path)))  # Write headers to the new file
                    writer = writer_cv
            print(f"Processed row {row_count}")
            writer.writerow(row)

        if category == "Poszukiwanie pracy":
            row_count_pracy += 1
        else:
            row_count_cv += 1

    out_csv_file_pracy.close()
    out_csv_file_cv.close()


def main():
    input_folder = "input"
    output_folder = "output"
    batch = True
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all CSV files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            if not batch:
                input_file_path = os.path.join(input_folder, filename)
                output_file_name = f"{os.path.splitext(filename)[0]}_processed.csv"
                output_file_path = os.path.join(output_folder, output_file_name)

                process_csv(input_file_path, output_file_path)
                print(f"Processed {filename} and saved to {output_file_name}")
            else:
                input_file_path = os.path.join(input_folder, filename)
                process_csv_batch(input_file_path, output_folder)
                print(f"Processed {filename} and saved to {output_folder}")


if __name__ == "__main__":
    main()
