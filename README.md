## Plant Quizzes

This repo contains the files for my first capstone project. It is a web app that provides quizzes to test the user's ability to recognize images of plants. 

A live version of the app is deployed on Heroku here: https://plant-quizzes.herokuapp.com/.

### Website Content

The core of the website is the set of quizzes that a person can take. Each quiz shows ten images of plants with four choices from which to select the correct common name for the plant. When the user submits the quiz, the total number correct is calculated, and the pictures are shown again with the correct common name. Under each picture is a link to a detail page fore each plant.

Users who are not signed in may pick from five quizzes; users who create an account can pick from any available quizzes. Initially, 17 quizzes are in the database. Users who take more than 10 different quizzes may request the creation of another quiz, with plants from a family the user selects.

Signed-in users have other benefits. They can view a list of all the quizzes they have tried, with the latest score and average score on each quiz. In addition, they can view a page with all the plants they have seen on a quiz for further study. There is also a page for each plant with details about the plant and links to Wikipedia and Google searches for even more information.

### Information Source

Information to create the quizzes comes from https://trefle.io/, which is an API that provides botanical data gathered from a variety of sources such as the USDA and Wikimedia.

Quiz questions come from the results of a search for plants (a specific category available in the API) filtered to include only ones with an image URL and a common name. If the quiz is for a specific plant family, the results are also filtered to include only ones from that family. Wrong answers come from the common names of plants in the search results that were not randomly selected for the quiz. 

### Technology Stack

The plant quizzes and user data are stored in a PostgreSQL database. The database schema is [here](schema.PNG). 

SQLAlchemy is the ORM connecting the database to the Flask app. 

The website is a Flask app. Forms use WTForms and password encryption uses Bcrypt. All of the pages are served with jinja2 templates. 

On the frontend, the Materialize framework (https://materializecss.com)  takes care of most of the styling.

If you're curious, [proposal.md](proposal.md) has more details on the original plan.

### To Use

The app is running at https://plant-quizzes.herokuapp.com/.

If you prefer to run it on your own machine:

- Clone this repo.
- Create a postgres database named plant_quizzes. (The tests require one named plant_quizzes_test.)
- Install Flask and the packages in requirements.txt.
- Run seed.py to populate the database with 17 pre-made quizzes.
- Start Flask and have fun!