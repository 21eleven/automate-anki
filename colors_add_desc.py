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

# Use the available methods to list the notes
#for cid in col.findNotes("tag:English"): 
for cid in col.findNotes("tag:colors"): 
    note = col.getNote(cid)
    front =  note.fields[0] # "Front" is the first field of these cards
    name = note.fields[1]
    print(name)

