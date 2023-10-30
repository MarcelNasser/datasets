# Open Datasets for Research

**Datasets herein are automatically generated. There are released under the MIT [licence](LICENSE) and liabilities.<br> 
We do not guarantee the correctness of those datasets. At best, they are as reliable as data sources and data pipelines...** 

## `numbers`

*data source*: google translate cloud [service](https://cloud.google.com/translate/docs/languages)

*data pipeline*: 

- requires
  - python 3.8+
  - google cloud cli
  - google cloud project with billing
  - translate api activated


- setup 

````bash
# install requirements
pip install -r requirements.txt
# checkout
python -m unittest pipelines/translate/test.py
# login to translate API
gcloud auth application-default login
````

- run

````bash
# bantu
python pipelines/translate/run.py translate -l xh ny lg ln zu -o csv > numbers/bantus.csv
````
