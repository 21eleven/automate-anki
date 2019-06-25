import sys, os
from dotenv import load_dotenv
import colorhexa as ch
from PIL import Image

sys.path.append("anki")
import anki
import anki.sched # not sure why i have to do this step...

Collection  = anki.storage.Collection

load_dotenv()
ankipath = os.getenv("ANKI_PATH")

print(ankipath)

cpath = os.path.join(ankipath, "collection.anki2")
print(cpath)

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

def update_note_field(note, field, new_value):
    note[field] = new_value
    note.flush()
    col.save()

def update_note(note, back, extra):
    note["Back"] = back
    note["Extra"] = extra
    note.flush()
    col.save()

# Use the available methods to list the notes
#for cid in col.findNotes("tag:English"): 
c = 0
for cid in col.findNotes("tag:colors"): 
    note = col.getNote(cid)
    
    for (name, value) in note.items():
        #print(name, value)
        if name == "Front":
            color = (
                    value.lower()
                         .split("src='")[-1]
                         .split('.png')[0]
                         .replace('-', ' ')
                         .replace('_', ' ')
                    )
            img_name = value.split("src='")[-1].split("'")[0]
            if color == "yellow":
                img_name = value.split('src="')[-1].split('"')[0]

        if name == "Back":
            back = value.split('\n')
            hexcolor = "#" + value.split("#")[-1].split(" ")[0]
    if len(back) == 2 and note["Extra"] == '':
        save = os.path.join(ankipath, "collection.media", img_name)
        extra = back[1].split("y>")[1].split("</")[0]
        back = back[0]
        print(extra)
        print(back)
        print(color)
        print(save)
        print(hexcolor)
        if color != "yellow":
            update_note(note, back, extra)
        im = Image.new("RGB", (200,200), hexcolor)
        im.save(save)
        c += 1
    print('/////////////////////////////////')

print(c)
