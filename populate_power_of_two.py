import sys
import os
from dotenv import load_dotenv

sys.path.append("anki")
import anki
import anki.sched # not sure why i have to do this step...
Collection  = anki.storage.Collection

load_dotenv()
ankipath = os.getenv("ANKI_PATH")
cpath = os.path.join(ankipath, "collection.anki2")
col = Collection(cpath, log=True) 

# Example front note
# Powers of 2:<div>2{{c1::<sup>0</sup>}} = {{c2::1}}</div>
# insert a crd the the firefox hot key for close tab is ctrl w
# col.models.allNames()
# use close
cloze_model = col.models.byName('Cloze')
col.decks.current()['mid'] = cloze_model['id']
deck = col.decks.byName("Default")


for i in range(1,17):
    note = col.newNote()
    note.model()['did'] = deck['id']
    n = 2**i
    field = "Powers of 2:<div>2{{c1::<sup>"+str(i)+"</sup>}} = {{c2::"+str(n)+"}}</div>"
    note.fields[0] = field
    tags = "math powers_of_two"
    note.tags = col.tags.canonify(col.tags.split(tags))
    m = note.model()
    m["tags"] = note.tags
    col.models.save(m)
    col.addNote(note)

col.save()
    



