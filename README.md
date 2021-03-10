## Plant Quizzes

This repo contains the files for my first capstone project. It will be an app that provides quizzes to test the user's ability to recognize images of plants. See [proposal.md](proposal.md) for more details on the original plant.

Information to create the quizzes comes from https://trefle.io/, which is an API that provides botanical data gathered from a variety of sources such as the USDA and Wikimedia.

The database schema for the project is [here](schema.PNG). It will be updated to reflect the actual schema (more fields added for some models) when the app is complete.

The current set of files produces a functioning website. I am working on polishing it and perhaps adding an additional feature or two, so check back soon.

### To Use

Create a postgres database named plant_squizzes. (The tests require one named plant_quizzes_test.)

Install Flask and the packages in requirements.txt.

Run seed.py to populate the database with 11 pre-made quizzes.