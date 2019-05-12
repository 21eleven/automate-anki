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

