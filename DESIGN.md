# PokerHub Design

## Back-End

### SQL

Our project uses a SQL database to store information about registered users as well as the poker hands played by these users. We created two tables: users and hands. The users table stores each user’s user_id, email, and password hash, and the hands table stores the hand information, the result of the hand, amount of money won or lost, and the appropriate user_id. 

The users table, accessed through the "register.html" file and “login.html” file, allows people to create new users and login to their accounts. The hands table, accessed through the “log.html” file, allows the user to add, delete and edit their hand history. Originally, we also included a third table that divided the hands up by play session, but we ran into several javascript bugs when attempting to match hands with appropriate play sessions. This is potentially an area of further improvement.

### Python and Flask

We used Flask, python’s micro-framework for web development, to run our web application. In app.py we imported sqlite for SQL, Flask, render_template, redirect, request, session, jsonify from flask so we could use flaks to run our app. We imported Session from flask_session so we could keep a user logged in for a particular session. We also imported generate_password_hash, check_password_hash from werkzeug.security in order to create and check passwords and imported datetime
The file also contains a list that includes all of 52 possible card names. We use this for the odds calculator. The file also contains the routes for each html file. The functionality of each is below:

    /register: A GET request displays the register.html template and allows the user to input their account information. A POST receives the email address, username, and password of the user and, if the credentials are valid, stores a new account in the users table of the poker database. Then, the user is redirected to the login page. Otherwise, an alert is displayed at the top of the page.

    /login: A GET request displays the login.html template and allows the user to input their login credentials. A POST request takes in the user’s username and password, checks the users table of the poker database to make sure that the credentials are accurate, and then redirects the user to the homepage. Otherwise, an alert is displayed at the top of the page.
 
    /logout: Ends the user’s session and redirects the user to the login page. 

    /: displays the index.html template

    /log: A GET request displays the log.html template, querying the hands table of the poker database to pass in overall summary statistics (total earnings, best hand, and worst hand) and the hand log. A POST request takes in the user’s hand search, and returns hand specific summary statistics (winnings with a particular hand and win percentage).
 
    /ajax_add: A POST request adds a row to the Hand History html table.

    /ajax_update: A POST request allows the user to edit an existing row of the Hand History html table.

    /ajax_delete: A POST request allows the user to delete a row of the Hand History html table.

NOTE: post requests to /ajax_add, /ajax_update, and /ajax_delete are all accomplished through JQuery, which is a frontend javascript framework that changes html code in response to user interactions with the webpage. Ajax is then used in order to send the data from the front end to the back end. 

    /odds: A GET request displays the odds.html template, giving the user the option to submit hands. A POST request takes in the cards that the user imputed – Player A’s hand, Player B’s hand, and, optionally, the board – and then, if all the inputs are appropriate, calls a function to calculate the odds that Player A and Player B would win. Finally, a user is redirected to a page that displays the probability of victory for each player, as well as more statistics about the type of winning hands – pair, flush, etc – and the likelihood that each type of hand would occur. 

    /tips: displays the template tips.html

We also included a helpers.py.
In the "helpers.py" file we created helper functions we imported into and called in app.py. Each function is described below:

    is_valid_email() takes in an email address and outputs true if it is a valid regex string and false otherwise.

    is _valid_password() takes in a password and outputs true if the string is more than 5 characters long and contains at least one uppercase character, lowercase character, number, and special character. Otherwise, the function outputs false.

    usd( )takes in a number and formats it to look like a dollar amount.

    percentage() takes in a decimal and converts and formats it to a percentage.

    apology() takes in a message and error code 400 and outputs an error image of a frog displaying the message and error code.

Eval.py contains the “simulate()” function that we imported to app.py. The simulate function takes in 10 inputs: the 9 potential cards (two for each player’s hand and four for the community board) and 1 variable that is set as either true or false depending on whether or not the user inputted cards for a community board. Then, the function accesses a program downloaded from the internet (essentially a python package), which takes these same outputs and returns a list that contains the likelihood of each hand winning as well as the likelihood of each possible hand type (pairs, straights, flushes, etc) for each hand. Next, the function takes that output list and reformats it through a series of “split” statements. The resulting list of lists is then returned. 

Also, our project contains a folder titled holdem_calc-master. This folder was downloaded from the internet (https://github.com/ktseng/holdem_calc) and contains functions that perform the math required for odds calculations. This is open source code available for free use for all, created by a Kevin Tseng. 

## Front-End

### HTML, CSS, JavaScript, and Ajax

For HTML and CSS, we created 9 HTML templates total and one unique stylesheet. We also linked to the bootstrap stylesheet, linked to table stylesheets, linked bootstrap’s javascript library, imported several google fonts, imported Ajax, and imported free-use icons from the internet.

Layout.html and styles.css as well as bootstrap styling ensured that our website maintained a good-looking and consistent design across all pages. The layout file includes a navigation bar and a footer. In styles.css we created universal variables and selected attributes that repeated multiple times throughout the web app, such as title1, title2, and body, in order to standardize fonts, text sizes, margins, and padding. We also used bootstrap buttons and other classes for consistency. 

We used the Ajax and javascript libraries to create the dynamic table to record hands on log.html.

The other 8 templates extend the layout.html file and link to the styles.css file. The pages are as follows:
apology.html: displays the apology message with the corresponding error and code.
index.html: the homepage titled “How to Play.” Where the user is introduced to poker and can learn how to play

    log.html: displays two accordions that open on click. The first accordion contains summary statistics that can be accessed via a form. The second accordion contains a dynamic table titled “Hands Played,: and allows the user to add their hands and see their stats using dropdown menus and buttons. The accordion function on the log.html page was also by far the hardest to style, because the page required several icons, hover functions, and animations. The accordions, by nature, also include many nested divs, making it hard to navigate through in the css.

    login.html: displays the login page where a user can enter their account information to access the website. The login page contains two divs side by side; the first containing a poker-themed image and welcome text, and the second containing a login form.

    
    odds.html: shows the interface where a user can input cards to find their odds of winning a hand.

    results.html: shows the results of the odds calculator. 

    tips.html: shows some tips and tricks on how to get better at poker