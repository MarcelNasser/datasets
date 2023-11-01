# Open Datasets for Research

**Datasets herein are automatically generated. There are released under the MIT [licence](LICENSE) and liabilities.<br> 
We do not guarantee the accuracy of those datasets. At best, they are as accurate as data sources and data pipelines.** 

## `numbers`

*content:*

- list all languages numbers from 1 to 99.<br>

- the dataset in broken into csv tables:

| table             | Languages                     |
|-------------------|-------------------------------|
| bantus.csv        | xh, ny, lg, ln, zu            |
| indo-european.csv | en, ru, uk, be, bg, .. ka, az |

*language codes [here](https://cloud.google.com/translate/docs/languages)*

*data source*: 
- google translate cloud [service](https://cloud.google.com/translate/docs/languages)
- romanization [lib](https://github.com/anyascii/anyascii) and [database](https://loc.gov/catdir/cpso/roman)
- according to [documentation](https://cloud.google.com/translate/docs/advanced/romanize-text), google translate API features a romanization algorithm as well. But API calls weren't working in the client library, the pricing of those calls wasn't clear and they weren't convenient as two calls are needed per text translation. We prefered this open source library, which works pretty well and is quite accurate.

*data pipeline*: 

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

## `Contribution`

This is an open source project but not very open yet, as the scope of this project is not well-defined. The project is for the moment a backyard to dump research data.
Maybe the project is short-lived. It will be a waste of time to onboard new people given the uncertainty here.

In any case, you can reach me on [LinkedIn](https://www.linkedin.com/in/marcelndeffo/).

Cheers.


