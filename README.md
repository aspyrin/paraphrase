# paraphrase
API that paraphrases text (syntax trees) without changing its meaning
test task https://dou.ua/calendar/46895/?from=tg


HOW TO RUN
in console:
    git clone <lical dir> git@github.com:aspyrin/paraphrase.git
    cd <project root dir>
    python3 -m venv env
    . env/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

you can use FastApi swagger
http://0.0.0.0:8000/docs

URL request example:
http://0.0.0.0:8000/paraphrase?tree=(S%20(NP%20(NP%20(DT%20The)%20(JJ%20charming)%20(NNP%20Gothic)%20(NNP%20Quarter))%20(,%20,)%20(CC%20or)%20(NP%20(NNP%20Barri)%20(NNP%20G%C3%B2tic)))%20(,%20,)%20(VP%20(VBZ%20has)%20(NP%20(NP%20(JJ%20narrow)%20(JJ%20medieval)%20(NNS%20streets))%20(VP%20(VBN%20filled)%20(PP%20(IN%20with)%20(NP%20(NP%20(JJ%20trendy)%20(NNS%20bars))%20(,%20,)%20(NP%20(NNS%20clubs))%20(CC%20and)%20(NP%20(JJ%20Catalan)%20(NNS%20restaurants))))))))&limit=5

-copy and past to browser, 
-change your <localhost> and <port>
-change parameters: tree & limit (optional)

curl -X 'GET' \
  'http://0.0.0.0:8000/paraphrase?tree=%28S%20%28NP%20%28NP%20%28DT%20The%29%20%28JJ%20charming%29%20%28NNP%20Gothic%29%20%28NNP%20Quarter%29%29%20%28%2C%20%2C%29%20%28CC%20or%29%20%28NP%20%28NNP%20Barri%29%20%28NNP%20G%C3%B2tic%29%29%29%20%28%2C%20%2C%29%20%28VP%20%28VBZ%20has%29%20%28NP%20%28NP%20%28JJ%20narrow%29%20%28JJ%20medieval%29%20%28NNS%20streets%29%29%20%28VP%20%28VBN%20filled%29%20%28PP%20%28IN%20with%29%20%28NP%20%28NP%20%28JJ%20trendy%29%20%28NNS%20bars%29%29%20%28%2C%20%2C%29%20%28NP%20%28NNS%20clubs%29%29%20%28CC%20and%29%20%28NP%20%28JJ%20Catalan%29%20%28NNS%20restaurants%29%29%29%29%29%29%29%29&limit=20' \
  -H 'accept: application/json'

limit by default = 20

NLTK - used to analyze the tree and search for potential branches for transposition.
Paraphrases generator is implemented in pure Python ( utils -> def create_new_paraphrase() ) 
