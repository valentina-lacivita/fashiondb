# FashionDB

A lightweight app to keep track of the Fashion MNIST images.

## Usage

First set up the project environment with `uv`, running the following command in the project root directory:

```bash
uv sync
```

and then kick off the app:

```bash
uv run python main.py
```

This will bootstrap a SQLite DB and seed it with a 100 image samples found in the folder `data` and spin the app -- by default on `127.0.0.1:8000`. To access the API docs to interact with the app, please open the Swagger UI at http://127.0.0.1:8000/docs .


## Outline

#### Image model
Given the project constraints and given SQLite does not natively support `ARRAY` types, the image 1D array is defined as a JSON/BLOB field called `data`. In addition to the base fields `id, label, data`, there are two additional fields to the image model:
1. `format_downscale_factor` to capture the desired visualization format of the image: `original, medium, low`.
2. `as_array` is a computed field that returns the image pixels in a square array format, in the resolution indicated by `format_downscale_factor`.

#### Database config
The database is configured in `db.py`, which also includes the code for seeding the database with the provided image sample.

#### Create, read, update and delete images
Functions to interact with the database directly (independently from the API) can be found in `crud.py`.

#### API
API routes are defined in `main.py`.



