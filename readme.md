# mpc-autofill

Automating MakePlayingCards's online ordering system.

If you're here to download the desktop client, check the [Releases](releases/) tab.

# Monorepo Structure
* Web project:
  * Located in `/MPCAutofill`,
  * Backend is Django 4 with Elasticsearch (sqlite is fine), frontend is Jquery,
  * Indexes images stored in the Google Drives connected to the project,
  * Facilitates the generation of XML orders for use with the desktop client,
  * Intended to be deployed as a web application but can also be spun up locally with Docker.
* Desktop client:
  * Located in `/autofill`,
  * Responsible for parsing XML orders, downloading images from Google Drive, and automating MPC's order creation interface.

Each component of the project has its own README and Python dependencies.

Please ensure that you install the `pre-commit` Python package and run `pre-commit install` before committing any code to your branch / PR - this will run `black` and `isort` on your code to maintain consistent styling.