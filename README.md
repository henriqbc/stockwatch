# Stockwatch

## Your personal stock price tracker!

Stockwatch is a service designed to help investors in keeping track of stock prices. It periodically checks the price of stock options registered by the user and, once the price hits the configured limits, it sends the user an email alert.

## Prerequisites

### Docker

Make sure you have [Docker](https://www.docker.com/) installed before starting.

### brapi

This project uses brapi API to collect information. Create or login to your [brapi](https://brapi.dev/) account and provide the token at the settings file by setting the value to REQUEST_TOKEN as a string, located in the /stockwatch/stockwatch/stockwatch/settings.py directory before starting.

## Getting started

1. Go to the project folder
```bash
cd stockwatch/stockwatch
```
2. Build and launch the docker image
```bash
docker-compose up --build
```
The app will be running at 127.0.0.1 or localhost, port 8000.

## Tests

To run all unit tests

```bash
docker exec -it django python manage.py tests
```

## Using the app

### **User**

#### Subscribe

The user can create or update their name and e-mail information; the e-mail provided will be the one to receive the alerts. 

Endpoint at /user/subscribe.

#### Home

The user can access this page, where they will find a link to the /user/subscribe in case they want to update their information. 

Endpoint at /user/home. Will redirect to /user/subscribe when unsubscribed.

#### Reset

The user can hit this endpoint to remove their user information. Used for testing, since app behaves overall differently when the user is unsubscribed. Only available to superusers. 

Endpoint at /user/reset. Will always redirect to /user/subscribe.

**Observation:**
Superusers can be created running this command on the project root.
```bash
docker exec -it django python manage.py createsuperuser
```

The terminal will then prompt the user to create their superuser.

Login as a superuser at /admin. Then go back to the app's base link.

### **Stocks**

#### Home

The user will always be redirected to this page when unsubscribed. The user will be instructed to subscribe before trying to access any monitoring options. Will always be redirected here from any other stocks endpoints if unsubscribed. Endpoint at /stocks.

#### New

The user can use this page to register a new stock to keep track of. Here, user provides the **Periodicity** in minutes of the check on the price and the price tunnel parameters: the **Upper bound of the tunnel** and the **Lower bound of the tunnel**; when this limits are breached, Stockwatch will automatically sent an e-mail alerting the user. A stock can only be added once to the list, but can always be updated later. 

Endpoint at /stocks/new. 
Will redirect to:
- /server-error when unable to fetch information on the available stock list from the api or if an error occurs on the server's side;
- /stocks when unsubscribed;
- /stocks/list after confirming;
- /stocks/new back with an error message if the request is invalid.

#### List

The user can see a list of all registered stocks. Clicking any of the options will take the user to that stock's page. The user can add new stocks or clear the whole list here. A confirmation pop-up will be triggered if the user tries to clear the list. 

Endpoint at /stocks/list. Will be redirected to:
- /stocks/delete when clearing list;
- /stocks/new when clicking to add new stock or if the list is empty;
- /stocks/<stock_name> when clicking one of the options;
- /stocks when user is unsubscribed;
- /server-error if any errors happen on the server's side.

#### (Stock's Name) Page

The user can see the last checked price of said stock and a line chart describing the behaviour of the stock's prince since adding the stock to the app. Here, the user can also update the tracking parameters on the stock, which will not delete the price history of the stock, or remove the stock from tracking, which will delete all information stored on the stock, which can be added again later, but without the previously stored information Trying to remove the stock will trigger a confirmation pop-up. 

Endpoint at /stocks/<stock_name>. Will redirect to:
- /stocks if user is unsubscribed;
- /stocks/new if an invalid stock_name is provided in the url;
- /server-error if any errors happen on the server's side;
- /stocks/delete/<stock_name> if the user clicks to delete the stock;
- /stocks/update/<stock_name> if the user clicks to edit the stock.

#### Update (Stocks's Name)

The user can edit their tracking preferences for the specified stock. Redirects the user to the stock's page upon confirming the new preferences. 

Endpoint at /stocks/update/<stock_name>. Will redirect to:
- /stocks if user is unsubscribed;
- /stock/<stock_name> after clicking to apply;
- /server-error if any errors happen on the server's side.

#### Clear list

This endpoint can be hit at /stocks/delete. It triggers the deletion of all the stocks. 

Will redirect to: 
- /stocks if user is unsubscribed;
- /server-error if any errors happen on the server's side;
- /stocks/list upon success.

#### Delete (Stocks's Name)

This endpoint can be hit at /stocks/delete/<stock_name>. It triggers the deletion of all the specified stock. 

Will redirect to:
- /stocks if user is unsubscribed;
- /server-error if any errors happen on the server's side;
- /stocks/list upon success.

### Other pages

#### Homepage

This is the welcome page to stockwatch. Endpoint is at app's base link.

#### Server error

Page displayed when internal server errors happen. Endpoint at /server-error.

### **Navbar**

The Stockwatch tab will always lead the user to the homepage.

The Stocks tab will take the user to /stocks when unsubscribed. When subscribed, it will redirect the user to /stocks/new if no stocks are registered or to /stocks/list if at least one is registered.

The User / (User's Name) tab will lead the user to /user/register when unsubscribed and to /user/home otherwise.
 
## License

This project is licensed under the MIT License.
