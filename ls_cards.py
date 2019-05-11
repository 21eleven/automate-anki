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
for cid in col.findCards("tag:*"): 
    card = col.getCard(cid)
    note = col.getNote(card.nid)
    front = note.fields[0]
    model = col.models.get(note.mid)

    print("//////////////////////////////////////////")
    print("//////////////////////////////////////////")
    print(card)
    print("//////////////////////////////////////////")
    print(note)
    print(front)
    print("//////////////////////////////////////////")
    print(model)
    print("//////////////////////////////////////////")
    try:
        template = model['tmpls'][card.ord]
    except IndexError:

        print("............INDEX ERR ON TEMPLATE.........")
        print(model['tmpls'])
        print(".")
        print(card.ord)
        print(".")
        print(card)
        print(".")
        print(front)
        print("..........................................")
        template = model['tmpls'][0]
    print(template)
