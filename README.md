# Expenses Management

Welcom to Expenses Management web application. This application will help you track on your expenses to help you manage your money. This application was create base on my problem. I spend money everyday, and I don't have enough money to save at the end of the month. So , I want to use this application to track my m oney and analized how much I spend in total base on the category of expenses. This application will help me manage my expenses better and I will have enough money to save by the end of the month.

## User Stories:

- As a user, I want to be able to login, so I can see my expenses board.
- As a user, I can register , so I can start using my expenses board.
- As a user, I can set my budget, so I can limit the money that I can spend.
- As a user, I can edit my budget, so I reduce or increase my money.
- As a user, I can create an expense list, so I can see my expenses list.
- As a user, I can update my expenses list, so I can see the updates of my expenses list.
- As a user, I can delete my expenses list, so I won't see it on my list anymore.
- As a user, I can see the percentage of my expenses, so I can compare how many percent that I spend from my budget.
- As a User, I can select the period of time to see the total that I spend on my expenses based on the category, So I can determine what category I should stop spending money with.
- As a user I can see my 10th last expenses list on my board, so I can see my updated list.

## Helpful Link:

![Google Chart](https://developers.google.com/chart)
![Google](https://developers.google.com/identity/protocols/oauth2)

## Technologies Used:

- Python
- Flask
- HTML
- CSS
- Bootstrap
- Google Chart API
- MySQL

## API End Points

| Verb   | URI Pattern        | Controller#Action |
| ------ | ------------------ | ----------------- |
| POST   | /login             | users#login       |
| POST   | /register          | users#register    |
| GET    | /user_dashboard    | users#index       |
| GET    | /new/budget        | budget#form       |
| POST   | /add_budget        | budget#create     |
| POST   | /edit_budget/:id>  | budget#update     |
| DELETE | /expense/:id       | expense#delete    |
| POST   | /add_expense       | expenses#create   |
| DELETE | /expense/:id       | expense#delete    |
| POST   | /edit_expense/:id  | expense#update    |
| POST   | /expense/list/date | expenses#index    |

## Unsovled Problem

- As a user, I can link my bank account data into the app, So I don't need to manually add expenses into my list.
- as a user, I can create many monthly budget, So I can see all of my expenses from the monthly budget.
- As a user, I can use my app in public deploy, so I can use my app everywhere.

## images

### ERD

![Expenses Management ERD](https://i.imgur.com/QV4zFxs.png)

### Wireframes

![Expenses Management Wireframes](https://i.imgur.com/soAb1PN.png)
