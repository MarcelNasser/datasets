# Pipeline(s) documentation

### Pipeline Translate

- requires
  - python 3.8+
  - google cloud [cli](https://cloud.google.com/sdk/docs/install)
  - google cloud project for [billing](https://console.cloud.google.com/)
  - translate api activated

- setup 

````bash
# install requirements
pip install -r requirements.txt
# checkout
python -m unittest pipelines/translate/test.py
# login to translate API
gcloud auth application-default login
# set billing project
export GOOGLE_PROJECT=tesselite
gcloud config set project $GOOGLE_PROJECT
````

- run

````bash
# bantu
python pipelines/translate/run.py translate -l xh ny lg ln zu -o csv > numbers/bantus.csv
# indo-european
python pipelines/translate/run.py translate -l ru uk be bg mk bs hr sr sk pl lv lt sl cs ro sq \
it el la co es ca fr de no sv fi hu hy ka az -o csv > numbers/indo-european.csv
````