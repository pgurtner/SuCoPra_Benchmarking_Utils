import re

"""
Extracts values for wanted_fields of LINPACK runs.

@param file_paths: list of file paths to HPL.out files
@param wanted_fields: list of data types you want (e. g. 'N' or 'Gflops')
@return: List[Dict{ [wanted field]: string value for field}]
"""
def extract_linpack_results (file_paths, wanted_fields):
    file_contents = map(_read_from_linpack_file, file_paths)
    content = ''.join(file_contents)
    
    regex = r'=+\nT/V.*\n-+\n.*'
    blocks = re.findall(regex, content)
    result = map(_extract_linpack_run(wanted_fields), blocks)
    
    return list(result)

def _read_from_linpack_file (file_path):
    file = open(file_path, 'r')
    content = file.read()
    file.close()
    return content


def _extract_linpack_run (wanted_fields):
    def a (summary):
        lines = summary.split('\n')

        fields = lines[1].split()
        values = lines[3].split()

        wanted_fields_indices = map(lambda f: (f, fields.index(f)), wanted_fields)
        targeted_values = map(lambda fi: (fi[0], fi[1], values[fi[1]]), wanted_fields_indices)

        result = {}
        for value in targeted_values:
            result[value[0]] = value[2]

        return result

    return a
