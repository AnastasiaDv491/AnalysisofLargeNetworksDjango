# Analysis of Large Networks App

This repository contains the Neo4j+Django App. It is deployed using railway.app at https://network-project-test-production.up.railway.app/
If you want to run the app locally, follow the steps:

1. Run `pip install -r requirements.txt` to install necessary packages.
2. Go to `settings.py` and comment out lines (mentioned in comments) that are used for deployment.
3. In the terminal run `python manage.py runserver`
4. Follow the URL to access to app locally.

Below you can fnd the description of every page:
1. Search: contains the main dashboard menu
2. Statistics: contains some brief summary statistics about the data used
3. About the project: contains the main report on the project
4. Codex: reference to Codex website from which the database was created
