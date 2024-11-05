def read_info_file(info_file_path):
    tag_mapping = {
        'Name:': 'name',
        'Abbreviation:': 'abb',
        'Tags:': 'tags',
        'Series Number:': 'series',
        'Publication Date:': 'publication_date',
        'Description:': 'description',
        'Required Citations:': 'citations',
        'Selected Studies:': 'studies'
    }

    infos = {'files': {}}

    with open(info_file_path, 'r') as file:
        line_cnt = 0
        lines = file.readlines()
        for line in lines:
            line_cnt += 1
            if not line:
                continue

            for tag, key in tag_mapping.items():
                if line.startswith(tag):
                    value = line[len(tag):].strip()
                    if key == 'tags':
                        infos[key] = [tag.strip() for tag in value.split(',')]
                    else:
                        infos[key] = value
                    break

            if line.startswith('file_name, modification_type, relates_to, title, description, publication_date'):
                break

        for line in lines[line_cnt:]:
            line = line.strip()
            if line:
                split_line = [part.strip() for part in line.split(',')]
                new_split_line = []
                tmp_split = ''
                inside_quotes = False

                for split in split_line:
                    if inside_quotes:
                        tmp_split += split
                        if split.endswith('"""') and len(split) > 3:
                            new_split_line.append(tmp_split[:-3])
                            inside_quotes = False
                        else:
                            tmp_split += ', '
                    else:
                        if split.startswith('"""') and len(split) > 3:
                            if split.endswith('"""'):
                                new_split_line.append(split[3:-3])
                            else:
                                tmp_split = split[3:]
                                inside_quotes = True
                        else:
                            new_split_line.append(split)
                new_file_info = {
                    'file_name': new_split_line[0],
                    'modification_type': new_split_line[1],
                    'relates_to': new_split_line[2],
                    'title': new_split_line[3],
                    'description': new_split_line[4],
                    'publication_date': new_split_line[5]
                }

                file_name = new_split_line[0].strip()
                infos['files'][file_name] = {key: value.strip() for key, value in new_file_info.items()}

    return infos


def file_description_line(file_dict, headers):
    values = []
    for h in headers:
        value = str(file_dict[h])
        if ',' in value:
            value = f'"""{value}"""'
        values.append(value)
    return ', '.join(values)


def write_info_file(file_path, info_dict):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Name: {info_dict['name']}\n\n")
        f.write(f"Abbreviation: {info_dict['abb']}\n\n")
        f.write(f"Tags: {', '.join(info_dict['tags'])}\n\n")
        f.write(f"Series Number: {info_dict['series']}\n\n")
        f.write(f"Publication Date: {info_dict['publication_date']}\n\n")
        f.write(f"Description: {info_dict['description']}\n\n")
        f.write(f"Required Citations: {info_dict['citations']}\n\n")
        f.write(f"Selected Studies: {info_dict['studies']}\n\n")

        if info_dict["files"]:
            headers = ["file_name", "modification_type", "relates_to", "title", "description", "publication_date"]
            f.write(', '.join(headers) + "\n")
            for file_descr in sorted(info_dict["files"], key=lambda x: x["file_name"]):
                f.write(file_description_line(file_descr, headers) + "\n")

