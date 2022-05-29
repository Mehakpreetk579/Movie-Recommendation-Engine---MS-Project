
# Movie Recommendation Engine

Recommendation Engine is a filtration program whose prime goal is to predict the “preference” of a user towards a domain-specific item or item. In our case, this domain-specific item is a movie, therefore the main focus of our recommendation system is to filter and predict only those movies which a user would prefer given some data about the user like to watch the movie.

It implements the concept of content based filtering algorithm and sorting algorithm.

## Website Link
```bash
  https://movie-recommendation-engine-ms.herokuapp.com/
```

## Project Flow

Step 1: Collect the data

- [Datasets are downloaded from Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)

Step 2: Pre-process the data

Step 3: Build a model

Step 4: Create a website to show the working of model

Step 5: Deploy the website
## Python requirements :

```bash
  from cgitb import text
  from email.mime import image
  from unicodedata import name
  import streamlit as st
  from PIL import Image

  import pickle
  from pathlib import Path

  import pandas as pd
  import requests

  import streamlit_authenticator as stauth
```
## Deployment

To deploy this project on local host, run

```bash
  streamlit run application.py
```


## Important Points

#### How to run the project on your computer

Download the application.py folder from the repository and write the below command in your terminal to run streamlit application on the local host 

```bash
  streamlit run application.py
```

