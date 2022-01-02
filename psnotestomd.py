import sys
import csv

def write_to_md(file_path: str, course_name: str, module_notes: dict):
    file_name, _ = file_path.rsplit('.csv', 1)
    md_file_path = f'{file_name}.md'
    print('Writing notes to: ', md_file_path)
    with open(md_file_path, 'w+') as md_file:
        md_file.write(f'# {course_name}\n\n')
        for module, notes in module_notes.items():
            md_file.write(f'\n## {module}\n')
            for raw_note in notes:
                note = raw_note.replace(r'\n', '\n')
                md_file.write(f'{note}\n\n')


def transform_to_md(file_path):
    with open(file_path) as csv_notes:
        reader = csv.DictReader(csv_notes)
        course = None
        modules = {}
        for row in reader:
            course = row['Course']
            # dict preserves insertion order as of python 3.8
            modules.setdefault(row['Module'], []).append(row['Note'])
    write_to_md(file_path, course, modules)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 2:
        print('Usage: python psnotestomd.py <file_path>')
        exit(1)
    
    file_path = sys.argv[1]
    print(f"file path {file_path}")
    transform_to_md(file_path)
    print('Done!')
