# tmdb-casting-lookup
Pet project to explore the TMDB REST API looking up for the casting for specified title, fetching the images, 
working the data with Apache Beam, and persisting the data into BigQuery. 

## Tech Stack
- Python 3.8 
- Apache Beam (Python SDK)
- Google Cloud Platform (BigQuery, CloudStorage, Dataflow)
- Poetry (build tool)
- Jupyter Notebook (for Exploratory Data Analysis)

## Up & Running 

- Set up an env var `TMDB_API_KEY` with your API Key
- Set up an env var for `GOOGLE_APPLICATION_CREDENTIALS`

- Pipeline Execution:
```
$ export TMDB_API_KEY=<tmdb_api_key>
$ export GOOGLE_APPLICATION_CREDENTIALS=<path/to/json/credentails.json>
$ python tmdb_cli.py search -q "<title>"
```

- Exploratory Data Analysis (EDA):
```
$ pip install requirements.txt
$ jupyter lab
```



## TODO
- [x] EDA: Movie API Details (images, casting, external_ids)
- [x] EDA: Movie Discovery by Release Date
- [x] EDA: TV Show API Details (images, casting, seasons, external_ids)
- [x] EDA: TV Discovery by Release Date
- [x] EDA: Search API (Textual search)
- [x] Apache Beam: Pipeline to transform Data
- [x] Apache Beam: WriteToBigQuery plugin w/ Streaming Insert
- [ ] Apache Beam: Perform Execution on Dataflow
