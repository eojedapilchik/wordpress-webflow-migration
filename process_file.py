import csv
import os
import requests
import re
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


def divide_elements(s: str):
    pattern = r'(\[su_note note_color="#fafafa" text_color="#233143"\](.*?)\[\/su_note\])'
    match = re.search(pattern, s, flags=re.DOTALL)  # re.DOTALL ensures that . matches newline characters as well

    su_note = match.group(1) if match else None

    return str(s), str(su_note)


def clean_elements(s: str) -> str:
    if not s:
        return ""
    pattern = r'\[su_([a-z]+)(?:[^\]]+)?\]'
    cleaned = re.sub(pattern, '', s)
    cleaned = (cleaned.replace('[/su_note]', '').replace('[/su_list]', '')
               .replace('[/su_box]', '').replace('[/su_highlight]', ''))
    return cleaned


def transform_su_box(match):
    color_class_map = {
        "#3be863": "green",
        "#ff826f": "red",
    }
    title = match.group(1)
    color = match.group(2)
    content = match.group(3).strip()
    color_class = color_class_map.get(color, "blue")
    return (f'<div class="{color_class}-highlight">'
            f'<div class="{color_class}-highlight-cont"><img src='
            f'\'https://assets.website-files.com/639975e5f44de65498a14a0e/63a0b5fcd66a3b979be8565b_icon-check.svg\'>'
            f'{title}'
            f'</div>'
            f'<div>{content}</div>\n</div><br>')


def transform_su_note(match):
    color = match.group(1)
    content = match.group(2).strip()
    if color == "#fafafa":
        return f'<div class="grey-div">\n{content}\n</div></br>'
    return f'<div class="blue-highlight">\n<div class="blue-highlight-flex">\n<div>{content}</div>\n</div>\n</div><br>'


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

    titles_to_skip = [title.lower() for title in titles_to_skip]
    with (open(input_path, 'r', encoding='utf-8') as csv_file):
        reader = csv.reader(csv_file)
        headers = next(reader)
        if 'content_html' not in headers:
            headers.append('meta Title')
            headers.append('meta Description')
            headers.append('su_note')
            headers.append('su_note2')
            # headers.append('content_html')

        yield headers  # Yield headers first

        for row in reader:
            title = row[2]
            if title.lower() in titles_to_skip:
                print(f"Skipping ${title}")
                continue

            content_idx = headers.index("Content")
            wrapped_content = wrap_with_p_tags(row[content_idx])
            content, su_note = divide_elements(wrapped_content)
            content = clean_elements(replace_elements(content)),
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

            content_html = html_response.get("content", "") if html_response else None

            su_note2 = html_response.get("su_note", "") if html_response else None

            row.append(meta_title)
            row.append(meta_description)
            row.append(su_note)
            row.append(su_note2)
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

    file_count = 1
    row_count = 0
    out_csv_file = open(os.path.join(output_folder, f"{base_name}_processed_{file_count}.csv"), 'w', newline='',
                        encoding='utf-8')
    writer = csv.writer(out_csv_file)

    for row in process_rows(input_path):  # Iterating over the generator
        if row_count == 0:  # if it's the header
            writer.writerow(row)
            row_count += 1
            continue

        if row_count % 50 == 0:  # For every 100 rows, switch the output file
            out_csv_file.close()
            file_count += 1
            out_csv_file = open(os.path.join(output_folder, f"{base_name}_processed_{file_count}.csv"), 'w', newline='',
                                encoding='utf-8')
            print(f"[+] A new file has been created: {base_name}_processed_{file_count}.csv")
            writer = csv.writer(out_csv_file)
            writer.writerow(next(process_rows(input_path)))  # Write headers to the new file

        print(f"Processed row {row_count}")
        writer.writerow(row)
        row_count += 1

    out_csv_file.close()


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
