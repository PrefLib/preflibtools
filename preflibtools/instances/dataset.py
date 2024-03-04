

def read_info_file(info_file_path):
    infos = {'files': {}}
    with open(info_file_path, 'r') as file:
        # We go line per line trying to match the beginning of the line to a known header tag
        lines = file.readlines()
        line_index = 0
        for line_index in range(len(lines)):
            line = lines[line_index]
            if len(line) > 1:
                if line.startswith('Name:'):
                    infos['name'] = line[5:].strip()
                elif line.startswith('Abbreviation:'):
                    infos['abb'] = line[13:].strip()
                elif line.startswith('Tags:'):
                    infos['tags'] = [tag.strip() for tag in line[5:].strip().split(',')]
                elif line.startswith('Series Number:'):
                    infos['series'] = line[14:].strip()
                elif line.startswith('Publication Date:'):
                    infos['publication_date'] = line[17:].strip()
                elif line.startswith('Description:'):
                    infos['description'] = line[12:].strip()
                elif line.startswith('Required Citations:'):
                    infos['citations'] = line[19:].strip() if line[
                                                              19:].strip() != "None" else ""
                elif line.startswith('Selected Studies:'):
                    infos['studies'] = line[17:].strip() if line[17:].strip() != "None" else ""
                elif line.startswith(
                        'file_name, modification_type, relates_to, title, description, publication_date'):
                    break
        # We are now reading the description of the files
        for line in lines[line_index + 1:]:
            line = line.strip()
            if len(line) > 0:
                split_line = line.split(',')
                new_split_line = []
                inside_quotes = False
                tmp_split = ''
                for split in split_line:
                    split = split.strip()
                    if len(split) > 0:
                        if inside_quotes:
                            if split[-3:] == '"""':
                                tmp_split += split[:-3]
                                new_split_line.append(tmp_split)
                                inside_quotes = False
                            else:
                                tmp_split += split + ', '
                        else:
                            if split[0:3] == '"""':
                                tmp_split += split[3:] + ', '
                                inside_quotes = True
                            else:
                                new_split_line.append(split)
                    else:
                        new_split_line.append('')
                infos['files'][new_split_line[0].strip()] = {
                    'file_name': new_split_line[0].strip(),
                    'modification_type': new_split_line[1].strip(),
                    'relates_to': new_split_line[2].strip(),
                    'title': new_split_line[3].strip(),
                    'description': new_split_line[4].strip(),
                    'publication_date': new_split_line[5].strip()
                }
    return infos