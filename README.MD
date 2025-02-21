# CS50x Final Project: Trivia Game 
#### By: Liann Finlayson 
#### Video Demo:  <https://youtu.be/H0TqnTSqDBU>


This final project is using HTML, Javascript, Python and SQL to combine 200 interactive and random trivia questions. 


# How will the game work?
The Trivia Questions are going to consider the following categories with questions that have multiple choice answers:
1. General Knowledge 
2. Science & Nature 
3. History 
4. Movies & TV Shows 
5. Animals 
6. Famous people & Celebrities 
7. Sports 
8. Technology & Computers 
9. Business & Economy 
10. Language & Linguistics 


* Users can enter multiple times with the same name to participate. No password registration will be required.
* Each user who enters their name will be randomly assigned a category and different questions
* Each correct multiple-choice answer will count as one point.
* The user with the highest number of correct answers across all categories will be the winner and will have a position on the Leaderboard.


# What features will the project have? #
## Front-end ## 
<h3>HTML</h3>
index.html: initial html page where the user can enter their name.
After entering their name, they will be presented with a random category and question.

#### HTML Structure ####
1. <h4>Head</h4>
* Adjusts layout based on device width
* Includes Bootstrap links and scripts
* Loads Google Fonts
* References the CSS file containing styles
* Sets the game title
* Loads a Javascript script that:
    * Initializes the game
    * Retrieves questions from the Python route
    * Checks the correctness of each answer
    * Updates the score
    * Displays the leaderboard whenever the user refreshes the page

2. <h4>Body</h4>
* Input field for the user's name
* "Start Game" button
* Cart title displaying the category
* Cart title displaying the question
* Leadeboard showing rank, name and score 


<h3>Javascript Functions Structure</h3>

__1. StartGame():__
* The value entered by the user in the element with the ID username is trimmed to remove extra spaces and converted to lowercase to avoid repetition of the same users.
*  A conditional ensures that the user has entered their name. If the name is empty, an alert is shown, and the game won't start
* Calls the fetchQuestion() function, which presents a random category and question

__2. fetchQuestion():__
* A conditional checks if the data returned from the Python route (via jsonify) contains a message. If it does, the element with the ID category will display "No more questions". The element with the ID question will show a the message "No more questions available", and the choices container will be cleared (set to empty)
* If no message is found, the ID element category will display the category, and the question will show the question.
* The choices cointainer will display the available choices, and initially, it will be empty (innerHTML ='')
* Buttons are created for each choice, with the following properties:
    * The button text will be the choice from the data returned
    * The button's appearance is styled using classList to apply Bootstrap button classes.
    * When the user clicks a button, the checkAnswer function is called to compared the user's selection with the correct answer store in the data. 
* Any errors are caught and logged to the console

__3. checkAnswer():__
* The function starts by checking if the user has entered a name. If the username is empty, it shows an alert asking the user to input their name.
* Based on wheter the selected answer matches the correct answer, an alert is shown on the screen telling the user if the answer is: Correct! or Incorrect!
* The function then sends the user's answers, along with the correct answer, to the /update_score route using a POST request. This request includes the user's name, their selected answer, and the correct answer in JSON format. The route is responsible for updating the score in the SQLite database. 
* If the request is successful, the leaderboard is updated by calling fetchLeaderboard(), which retrieves and display the updated leaderboard
* Any errors that occur during the process (such as issues with the fecth request) are caught and logged to the browser's console for debugging purposes.
* Finally, fetchQuestion() is called to fetched the next question.

__4. fetchLeaderboard():__
* This function fetches the leaderboard data from the server
* It declares a variable called leaderboardTable that references the HTML element with the ID leaderboard
* The innerHTML of the leaderboardTable is initialized with the table headers: "Rank", "Name" and "Score"
* For each entry in the retrieved data, the leaderboard is updated with the participant's rank (index + 1), name and score
* Any errors during the fetch process are caught and logged to the console
* To ensure the leaderboard is updated every time the page is loaded, the window.onlaod method is used to called fetchLeaderboard() as soon as the page loads.

#### CSS ####
1. Update the look and feel of the web page to improve user experience:
* Centering the body and "Start game" button
* Changing the color of the "Start game" button and adding a hover feature

## Back-end ##
<h3>Python: app.py</h3>

1. Import libraries: flask, sqlite3, random and dictionary called trivia questions that is in an separate file
2. Established connection with sqlite3 using conn.

3. Python route /get_question:
    * A function name get_question() is defined for the /get_question route
    * Session Management: it checks if "answered_questions" exists in the session. If not, it initializes it as an empty list
    * Building all_questions list: 
        * Creates an empty list called all_questions
        * It then loops through the trivia_questions dictionary. For each category, it adds the category name to the question dictionary and appends it to all_questions.
    * Filtering answered questions: It filters out the questions that have already been answered by the user (using the answered_questions list in the session).
    * No available questions: if there are no available questions left in available_questions, it returns a JSON response with the message "No more questions available"
    * Selecting a random question: if there are available questions, it selects a random question from available questions
    * Updating session: 
        * The question’s ID is added to the answered_questions list in the session to track that it has been answered.
        * It sets session.modified = True to notify Flask that the session has been updated. 
    * Returning data: it returns a JSON response with the selected question's category, question, choices, and correct answer.

4. Established /update_score route: 
    * Route definition: the route/update_score is define to handle POST requests. This route is responsible for updating the score in the leaderboard
    * Request data: the data is received as JSON via request.get_json(). It contains the user's name, their selected answer, and the correct answer.
    * Score calculation: a variable points is set to 1 if the user's selected answer is correct, and 0 if it's incorrect
    * Database connection: a connection to the SQLite database is established using the get_db_connection() function, and a cursor is created for executing SQL queries.
    * Checking existing score:
        * The code queries the leaderboard to check if the player (identified by their name) already has a score. It retrieves the existing score using the SQL query: SELECT score FROM leaderboard WHERE name = ?.
        * If the player already exists in the leaderboard:
            * The existing score is updated by adding the points (either 1 or 0).
            * The score in the database is updated using the SQL query: UPDATE leaderboard SET score = ? WHERE name = ?.
        * If the player does not exist in the leaderboard:
            * A new entry is created in the leaderboard with the player’s name and their score (either 0 or 1).
            * This is done using the SQL query: INSERT INTO leaderboard (name, score) VALUES (?, ?).
    * The changes are committed to the database with conn.commit() and the database connection is closed with conn.close()
    * A JSON response is returned with the message "Score updated successfully", confirming that the operation was successful.

5. Established /leaderboard route that:
    * Route definition: fetches the top 10 players from the leaderboard
    * Database query: Selects the player's name and score from the leaderboard table, orders by score in descending order, and limits the result to the top 10 players
    * Response: returns the top 10 players as a JSON array with their names and scores. 

6. Established / route that:
    * Shows the home index.html


<h3>SQLite3 database</h3>
There is a SQLite3 database that stores the results of each game, with the following columns:

1. id: the unique identifier and primary key. Type: INTEGER AUTOINCREMENT
2. name: name of the person that is participating in the game. Type: TEXT NOT NULL
3. score: the total points accumulated in each game session. Type: INTEGER

Points must be updated after each completed game. 
This leaderboard will be limited to the top 10 positions and will be displayed on the game’s initial page (index.html).


# What new skills did I need to acquire? #
1. Reflect random selection of category and questions generated in Python, in HTML so the users can see it
2. Save correct choices and update the SQLite3 database every time a user selects a correct choice


# What topics did I need to research?
1. Questions for every category/topic in the trivia 


# Review of Javascript terms
1. fetch: built-in Javascript function used to make HTTP requests, such as retrieving data from the server. It's used to retrieve data from the /get_question and /leaderboard routes on the server.
2. then(): is a method that runs after the fetch request has completed succesfully. It receives the response object (the result of fetch)
3. response.json(): method that converts the response from the server (usually in JSON format) into a JavaScript object. Since the fetch API response is not automatically in a usable format, this step is necessary to parse the data.
4. The arrow => is part of the arrow functions. A concise way of writing functions in JavaScript. It’s the equivalent of writing a normal function, but with a shorter syntax 
Normal function: function(response) { return response.json(); }
Arrow function:  response => response.json()
5. .then (data => {}) This then() handles the data that comes from the previous json() method. It’s where you can work with the actual data (like data.category, data.question, etc.).
The arrow function data => {} is used here to define what should happen with the data once it’s parsed into a JavaScript object.
6. let:  is used to declare a variable in JavaScript. It allows the variable’s value to be updated later. 
7. .catch(error => console.error('Error', error)); : .catch() is used to handle errors that might occur during the fetch operation. console.error('Error', error) logs the error message to the browser’s console.
8. forEach: array method in JavaScript that loops through each element of an array and executes a given function for each element. In this code, data.choices is an array containing the available choices for the question.
9. row.appendChild: appendChild is a method in Javascript used to add a new child element to an existing parent element in the DOM. In this code, row.appendChild(button) adds each button (created dynamically) to the row element. This means that each button is appended as a child to the row container.
10. window.onload: as soon as the page loads the information is going to be shown to the user

# Review of Flask terms
1. jsonify: it converts Python data types (like dictionaries, lists, etc.) into a JSON response, which is then sent to the client (in this case, the JavaScript code you’re working with). This allows the JavaScript client (using fetch in your case) to receive and handle the data as a JSON object.


# Future iterative improvements
1. Timer constraint: it could be more intersting if I put a timer constraint that give the user only 30 seconds per question to avoid users cheating.
2. More questions: in the future, add more categories and questions
3. Remove alert: Instead of an alert that the user confirms clicking the button "OK" it would be nicer to show that correct/incorrect answer in the html and move along the category/question automatically. 
4. User security: add a password to prevent users from impersonating or using other users’ names
5. User memory: instead of not repeating questions per session, remember which questions each user has answered
6. CSS improvements: have a more fun interface; add images related to the question for each category.
