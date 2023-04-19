import re

"""
Extracts values for wanted_fields of LINPACK runs.

@param file_paths: list of file paths to HPL.out files
@param wanted_fields: list of data types you want (e. g. 'N' or 'Gflops')
@return: List[Dict{ [wanted field]: string value for field}]
"""
def extract_linpack_results (file_paths):
    file_contents = map(_read_from_linpack_file, file_paths)
    content = ''.join(file_contents)
    
    regex = r'=+\nT/V.*\n-+\n.*'
    blocks = re.findall(regex, content)
    result = map(_extract_linpack_run, blocks)
    
    return list(result)

def _read_from_linpack_file (file_path):
    file = open(file_path, 'r')
    content = file.read()
    file.close()
    return content


def _extract_linpack_run (run_summary):
    lines = run_summary.split('\n')

    fields = lines[1].split()
    values = lines[3].split()

    if len(fields) != len(values):
        raise Exception(f'field number is different from values number:'
            + ' {len(fields)} fields, {len(values)} values')

    field_value_pairs = zip(fields, values)

    result = {}
    for value in field_value_pairs:
        result[value[0]] = value[1]

    return result
