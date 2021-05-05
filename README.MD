# Splitwise
This project is for calculating and managing accounts and transactions especially when a group of people go out together and contribute unequally. It calculates the amount to be lent or received and to who and from whom and stores them in the accounts of both the lender as well as receiver along with the amount to be exchanged.

* Transactions : Add the People and Amount they spent : Incudes names of all users, amounts and the transaction date
* Accounts : These are created automatically from each transaction (backend script) : Includes transactiond date, transaction Iid, lender, receiver and amount to be exchanged

## Overview
This project is created using AngularJs framework and it is built using Python Flask backend (PostgreSQL Database). The Styling Rules are present in the "style.css" file.

The component views are manipulated using AngularJs only (ng-shoq, ng-hide) without any use of javascript to manipulate the DOM.

## Functions and Filters used within AngularJs
* Date filter to display formatted date
* addEntry : to add new entry for transactions
* seepasswordfunc : to view passwords as string
* addTransSection : view the transaction section
* changeToSignUp/SignIn : switch between login/register 
* logout function : logs you out
* clearAddTrans : clear the add transaction list
* fetchUsers/Transactions/Accounts : makes API request to get all users/transactions/accounts
* hideUsers,hideTrans (for admin),hideAcc, hideUserTrans (for user based on trasactions created by him only) : hide respective sections
* login and register
* addtransaction : add the new transaction to database by sending a request to the API
* checkLogin : checks if currentUser is not null and makes necessary changes to scope variables

## Files and Folders :
* Index.html : Main html file
* app.js : AngularJs file
* /backend : Database models (models.py) and main server script (app.py)
* /images : Contains al images used in the frontend
* test.rest : API calls and testing
* User_Janmejay16_Demo and User_admin_demo : Video Recordings of the application
* style.css : Contains the style sheets