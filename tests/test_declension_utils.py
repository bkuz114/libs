import sys
import os
sys.path.append("..")
import declension_utils as marker

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(SCRIPT_DIR, "noun_mark.html")

with open(filepath, 'r') as file:
    file_content = file.read()

marked = marker.mark_string(
        file_content, "{", "}", "[", "]", "[[", "]]", "*")

print("===== MARK ENTIRE FILE CONTENTS ====")
print(file_content)
print(marked)

print("===== MARK A SINGLE EXAMPLE SENTENCE ====")
string = "[Иавн*а] сын."
marked = marker.mark_sentence(
        string, "[", "]", "[[", "]]", "*")
print(string)
print(marked)
