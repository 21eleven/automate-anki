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
    
    old_img = note['Front'].split("src=")[-1][1:-2]
    print(old_img)
    new_img = old_img.lower().replace('-', '_')
    print(new_img)
    print(note["Front"])
    new_front = "<img src='{}'>".format(new_img)
    print(new_front)
    assert new_img != old_img
    new_path = os.path.join(ankipath, 'collection.media', new_img)
    old_path = os.path.join(ankipath, 'collection.media', old_img)
    print(old_path)
    print(new_path)
    assert new_path != old_path
    os.rename(old_path, new_path)
    update_note_field(note, "Front", new_front)

    c += 1
    print('/////////////////////////////////')

print(c)
