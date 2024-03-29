import sys, os, codecs, re, shutil
from dotenv import load_dotenv
sys.path.append("anki")
from anki.storage import Collection
import anki.sched

load_dotenv()
PROFILE_HOME = os.getenv("ANKI_PATH")
OUTPUT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))+'/out'

# Utility methods

def rawText(text):
    """ Clean question text to display a list of all questions. """
    raw_text = re.sub('<[^<]+?>', '', text)
    raw_text = re.sub('"', "'", raw_text)
    raw_text = raw_text.strip()
    if raw_text:
        return raw_text
    else:
        return "Untitled"

def extractMedia(text):
    regex = r'<img src="(.*?)"\s?/?>'
    pattern = re.compile(regex)

    src_media_folder = os.path.join(PROFILE_HOME, "collection.media/")
    dest_media_folder = os.path.join(OUTPUT_DIRECTORY, "medias")

    # Create target directory if not exists
    if not os.path.exists(dest_media_folder):
        os.makedirs(dest_media_folder)

    for (media) in re.findall(pattern, text):
        src = os.path.join(src_media_folder, media)
        dest = os.path.join(dest_media_folder, media)
        shutil.copyfile(src, dest)

    text_with_prefix_folder = re.sub(regex, r'<img src="medias/\1" />', text)

    return text_with_prefix_folder


# Load the anki collection
cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True)

# Iterate over all cards
cards = {}
for cid in col.findCards("tag:*"):

    card = col.getCard(cid)

    # Retrieve the node to determine the card type model
    note = col.getNote(card.nid)
    model = col.models.get(note.mid)
    tags = note.tags

    # Card contains the index of the template to use
    try:
        template = model['tmpls'][card.ord]
    except IndexError:
        if len(model['tmpls']) != 1:
            print(model['tmpls'])
            raise 
        else:
            template = model['tmpls'][0]

    # We retrieve the question and answer templates
    question_template = template['qfmt']
    answer_template = template['afmt']

    # We could use a convenient method exposed by Anki to evaluate the template
    rendering = col.renderQA([cid], "card")[0]
    # Only one element when coming from a given card
    # Could be more when passing a note of type "Basic (with reversed card)"

    question = rendering['q']
    answer = rendering['a']

    question = extractMedia(question)
    answer = extractMedia(answer)

    css = model['css']

    html = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Card Answer</title>
  <style>
  %s
  </style>
</head>
<body>
  <div class="card">
  %s
  </div>
</body>
</html>""" % (css, answer)

    card_filename = "card-%s.html" % cid
    card_file = codecs.open(os.path.join(OUTPUT_DIRECTORY, card_filename), \
                            "w", "utf-8")
    card_file.write(html)
    card_file.close()

    cards[cid] = {
        'name': rawText(question),
        'file': card_filename,
        'tags': tags
    }


# Generate a list of all cards
card_list = '['
for cid, props in cards.items():
    print(repr(props['name']))
    cleaned_name = props['name'].replace('\n', '')
    card_list += "{ 'name': \"%s\", 'file': '%s', 'tags': [ %s ] },\n" % (
        cleaned_name, #props['name'],
        props['file'],
        "\"" + "\",\"".join(props['tags']) + "\"")
card_list += ']'

html = """<!doctype html>
<html lang="fr" ng-app="ankiApp">
<head>
  <meta charset="utf-8">
  <title>Anki Export</title>
  <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.7/angular.min.js">
  </script>
  <style>
body {
    background-color: #0079bf;
}
#search {
    position: fixed;
    height: 70px;
    width: 100%%;
    padding-top: 20px;
    text-align: center;
}
#search input {
    width: 80%%;
    height: 30px;
    border-radius: 15px;
    text-align: center;
    border: none;
    box-shadow: 2px 2px #222;
}
#list {
    position: fixed;
    width: 50%%;
    top: 70px;
    bottom: 0;
    left: 0;
}
#list ul {
    list-style-type: none;
}
#list li {
    background-color: white;
    border: 1px solid silver;
    border-radius: 2px;
    width: 90%%;
    padding: 5px 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    cursor: pointer;
}
#card {
    position: fixed;
    width: 50%%;
    right: 0;
    top: 85px;
    bottom: 0;
}
iframe {
    background-color: white;
    border: none;
    box-shadow: 5px 5px 3px #333;
}
.tag {
    float: right;
    margin-right: 10px;
    padding: 2px 5px;
    background-color: orangered;
    color: white;
    font-size: 12px;
    font-family: Arial;
}
  </style>
  <script>
angular.module('ankiApp', [])
  .controller('AnkiController', function() {
    var anki = this;
    anki.cardList = %s;
    anki.selectedCard = anki.cardList[0];

    anki.select = function(card) {
      anki.selectedCard = card;
    }
  });
  </script>
</head>
<body>
  <div ng-controller="AnkiController as anki">
      <div id="search">
        <input type="text" ng-model="anki.search" placeholder="Search...">
      </div>
      <nav id="list">
        <ul>
          <li ng-repeat="card in anki.cardList | filter:anki.search \
                                               | orderBy:'name'""
              ng-click="anki.select(card)">
            {{card.name}}
            <span class="tag" ng-repeat="tag in card.tags">{{tag}}</span>
          </li>
        </ul>
      </nav>
      <div id="card">
        <iframe ng-src="{{anki.selectedCard.file}}" width="80%%">
        </iframe>
      </div>
  </div>
</body>
</html>""" % (card_list)


index_filename = "index.html"
index_file = codecs.open(os.path.join(OUTPUT_DIRECTORY, index_filename), \
                         "w", "utf-8")
index_file.write(html)
index_file.close()
