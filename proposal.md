# Plant Quizzes
### Goal and Audience
This web app will allow users to test thier knowledge of plants from around the world. It will produce quizzes where each question is a plant image with multiple choices from which to select the correct common name. Users can see how many they got right and find out more information about each plant on their quiz. 

There will be two difficulty levels. Easy quizzes will have wrong answers selected from different plant families from the correct answer, while hard quizzes will have the wrong answers selected from similar plants.

The audience is anyone interested in plants, or nature more generally. Young students may enjoy the easy level, while plant lovers can test their expertise with difficult quizzes.

User accounts will allow users to track their progress and revisit previously-taken quizzes.

### Data Source
The Trefle.io API provides a huge source of botanical data, collected from a variety of sources. Their 120 requests per minute limit should not be an issue if the app only gets light use. It appears, with minimal poking around, that they have over 25,000 plants in their database with both a common name and an image URL. These data should be sufficient for creating many different quizzes.

The API appears to be standard format, requiring a token, with various endpoints corresponding to the botanical hierarchy (kingdoms, divisions, families, etc). The 'plants' endpoint is between genus and spicies and seems a reasonable one to use for general knowledge about plants. The API provides querying, filtering, and sorting options.

### Database Schema
This is a work-in-progress. One table will be for user accounts (id, username, password - usual security for this), one table for quizzes (id, maybe nothing else?), and one for quiz questions (id, image_url, four choices, correct choice - needs to be planned out). There will be two tables for the many-to-many relationships between user and quiz and between quiz and questions. Or perhaps questions will belong to only one quiz? That user-quiz table would be quiz attempts: with user_id, quiz_id, date, and result?

### User Flow
Anyone can take a quiz, but to save results, they will need an account (may need to figure out how to save already-taken quiz to newly-created account). The homepage will give options for easy quiz, hard quiz, log in, create account. Quiz page will be a form with radio button choices, probably require all (10?) questions to be answered. After submission, the results will be shown marked correct or not, with correct answers shown. Logged-in users will have a page showing their quizzes with the latest result, each of which they can choose to take again.

### Stretch Goal
Allow users to customize their quizzes - perhaps focus on a particular plant family? Or give them the option for a quiz from questions they've gotten wrong in the past (this would mean quiz-to-question relationship would have to be many-to-many.) Maybe some exploration options beyond showing basic info about each plant at the end of each quiz.