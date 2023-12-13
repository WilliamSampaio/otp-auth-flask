# OTP Auth With Flask

OTP authentication example project in Python using the Flask framework. It helped me understand (a little) this authentication system.

We have the following routes:

* `/` Base route that renders the login template
* `/home` Route that renders the screen when login is validated
* `/logout` Route where the session is destroyed
* `/register` The entire user registration flow
* `/login` Validates the user's login form
