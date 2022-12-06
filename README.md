# PokerHub Manual
## Introduction
PokerHub is a web app, intended to provide information on how to play poker, improve skills, and provide resources to use while playing and to analyze your performance after the game. 
## Getting Started
To access the website, open it in VS Code, and make sure you have python, git, pip, flask, flask session, the SQLite extension, and workzeug security downloaded. Next, run app.py using flask to open the website. Initially, upon accessing the website, you are presented with a login page. The login page allows you to log in with a username and password, or register as a new user. Pressing the “sign up” button directs you to the “register” page so you can create an account by entering your email and password if you do not already have an account. Once you register, the site takes you back to the login page, where you can use the account you just created to log in. Once you register or log in, you are directed to the homepage. The website consists of four pages, which can all be reached by a navigation bar that changes to a drop-down menu when the page shrinks. The navigation bar also includes a logout button that logs you out and returns you to the login page. 
## Pages
The homepage for PokerHub is a “How to Play” page. The “How to Play” page provides detailed instructions on how to play poker, starting with the setup and basic rules, then explaining how to play each hand, and finally describing how a player wins the game. The instructions are accompanied by related images. 

On the second page, called “Tips and Tricks”, the user can learn to find information and resources to help them improve at the game. For each poker strategy, there is an image, the name of the strategy, a brief definition of the strategy, and two links to resources where the user can learn more about the strategy. The strategies are divided into three intermediate strategies (bluffing, tells, and hand reading) and two advanced strategies (ranges and 3-betting) 

The third page, called “Odds Calculator”, allows users to input a hand of cards for themselves, a hand for their opponent, and any cards that have already been dealt out on the board (which, according to the rules of the game, can either be 0, 3, 4, or 5 cards). Then, the program will calculate the odds of each possible outcome (user winning, opponent winning, tie) and display them. Additionally, the resulting page will display two tables that depict the likelihood of each possible final hand for each player (i.e. likelihood of ending the hand with a pair, two pairs, etc.)

The fourth page, called “Hand History,” has two functions. First, the page contains a dynamic table, in which users can log the hands they have played. Users can add new hands to the table, edit existing hands, and delete hands from the log. In addition, the page will tell users some summary statistics about the hands they have played. For instance, a user can type in a hand and get the percentage of times they have won with that particular hand, as well as the total amount of money they have won with that hand. The summary statistics page will also provide a running tally of the total number of hands played, the total amount of money the user has won or lost, the hand they have won the most money with, and the hand they have lost the most money with. 

Please find our project presentation video at the following link: https://youtu.be/Gqeq4v-TobM
