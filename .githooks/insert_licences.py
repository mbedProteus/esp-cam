#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright (c) 2025 Kien Le
# Email: thaikien.kc@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

import os
import datetime
import argparse
import re

LICENSE_HEADER = f'''-----------------------------------------------------------------------------
Copyright (c) {datetime.datetime.now().year} Kien Le
Email: thaikien.kc@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-----------------------------------------------------------------------------'''

LICENSE_HEADER_START_PATTERN = r"Copyright \(c\) (\d{4}-\d{4}|\d{4}) Kien Le"
LICENSE_HEADER_END_PATTERN = r"THE SOFTWARE.$"

def insert_comment_symbol(content: list[str], comment_symbol):
    new_content = []
    if comment_symbol == "//":
        new_content = [f"// {line}" for line in content]
    elif comment_symbol == "#":
        new_content = [f"# {line}" for line in content]
    elif comment_symbol == "/*":
        if len(content) == 1:
            new_content = [f" * {content[0]}"]
        else:
            new_content = [f"/* {content[0]}"] + [f" * {line}" for line in content[1:-1]] + [f" * {content[-1]} */"]
    else:
        return None
    
    for i, line in enumerate(new_content):
        if not line.endswith("\n"):
            line = line + "\n"
            new_content[i] = line
        
    return new_content

def find_license_header(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            return None
        copyright_line_number = 0
        for i, line in enumerate(lines):
            if re.findall(LICENSE_HEADER_START_PATTERN, line):
                copyright_line_number = i
                break
        
        if copyright_line_number == 0:
            return None
        
        for i, line in enumerate(lines):
            if re.findall(LICENSE_HEADER_END_PATTERN, line):
                return i + 1

    return None

def add_license_header(file_path, comment_symbol):
    new_content = []
    end_of_license_header = find_license_header(file_path)
    if end_of_license_header is not None:
        print(f"Updating license header in {file_path}")
        with open(file_path, "r") as fr:
            year_in_file = ""
            copyright_line_number = 0
            lines = fr.readlines()
            for i, line in enumerate(lines):
                if i < end_of_license_header:
                    if "Copyright" in line:
                        year_in_file = re.findall(r"\d{4}-\d{4}|\d{4}", line)[0]
                        copyright_line_number = i
                        break

            if year_in_file is not None and year_in_file == str(datetime.datetime.now().year):
                return
            else:
                new_year = ""
                if "-" in year_in_file:
                    new_year = year_in_file.split("-")[0]
                    new_year = new_year + "-" + str(datetime.datetime.now().year)
                else:
                    new_year = year_in_file + "-" + str(datetime.datetime.now().year)
                lines[copyright_line_number] = insert_comment_symbol([f"Copyright (c) {new_year} Kien Le\n"], comment_symbol)[0]
                new_content = lines
    else:
        print(f"Inserting license header in {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()
        content = insert_comment_symbol(LICENSE_HEADER.split('\n'), comment_symbol)
        if content is None:
            return
        if lines[0].startswith("#!"):
            new_content.append(lines[0])
            new_content.extend(content)
            new_content.extend(lines[1:])
        else:
            new_content.extend(content)
            new_content.extend(lines)

    with open(file_path, "w") as file:
        file.writelines(new_content)

def comment_symbol_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".py":
        return "#"
    elif ext == ".c" or ext == ".h":
        return "/*"
    elif ext == ".cpp" or ext == ".hpp":
        return "/*"
    elif ext == ".sh":
        return "#"
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert or update license headers in a source file.")
    parser.add_argument("file_path", help="Path to the source file")
    args = parser.parse_args()

    comment_symbol = comment_symbol_for_file(args.file_path)
    if comment_symbol:
        add_license_header(args.file_path, comment_symbol)
