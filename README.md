# Online Banking Management System

This is a full stack website built using Python that allows users to sign up and login to online virtual bank accounts, where they can make transactions,
avail loans, and invest in fixed deposits. 

The back end of the website is implemented using the Flask micro-web framework and a SQLAlchemy database that stores user details such as usernames and 
passwords, previous transactions, and current and previous loans and investments. The front end was designed using HTML5 and CSS3 along with the Bootstrap
front end framework. 

Improved the security of the website by applying to SHA256 hashing algorithm in the Werkzeug security library for secure passwords. The website also prevents 
first order SQL Injection and XSS (Cross Scripting) attacks by sanitizing user inputs and limiting the use of special characters. The secuirty measures detect
any form of SQL or JS code entered in all input fields and disregards any such entries. 

To view the website for yourself, clone the repository to your local system. Next, in VSCode, open the cloned repository using the open folder option. 
To run the website on your local network, enter the following commands into the terminal. 

export FLASK_APP=app
flask run

A message saying "Running on http://127.0.0.1:5000/" should appear. Click the URL to go to the website. The email address for the test account is 
"johnwick@gmail.com" with password "john123". Feel free to explore the functionalities of the website by playing around with making transactions, loans, and 
investments. You may also create a new account by signing up. 
