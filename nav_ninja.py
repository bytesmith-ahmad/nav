from configparser import ConfigParser
from cutie import select


filenames = ConfigParser()
filenames.optionxform=str
filenames.read('filenames.ini')
sections : list[str] = filenames.sections()
# items : dict[str,str] = {}

i = 0
items = []
captions = []
for section in sections:
    captions += [i]
    items += [section + ":"]
    i += 1
    for k,v in filenames.items(section):
        items += [f"\033[{33}m{k}\033[0m : {v}"]
        i += 1

chosen_path = select(
    items,
    caption_indices=captions,
    deselected_prefix="   ",
    selected_prefix=" \033[92m>\033[0m ",
    selected_index=1
)

print("\nGOING TO " + items[chosen_path])