import sys, os
from dotenv import load_dotenv

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

# Use the available methods to list the notes
#for cid in col.findNotes("tag:English"): 
for cid in col.findNotes("tag:colors"): 
    note = col.getNote(cid)
    for (name, value) in note.items():
        print(name, value)
    break


