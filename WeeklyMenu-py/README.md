Recipe Planner
========================

**Recipe Planner** lets you manage your own recipes, including ingredients, and link to those posted by others. From your list of recipes it creates weekly menus by selecting random recipes. This greatly simplifies weekly meal planning and lets you keep track of all your favorite recipes in one convenient location.

Work is underway to automatically add the ingredients for each recipe to grocery websites: Amazon Fresh, Whole Foods Market, Instacart, and several others.

### Setup
This should run from a production web server, e.g. httpd. These notes are for using django's development server.

* Install python 3.8 or higher
* Download project to a install directory
* Install dependencies
  ```
  cd {installDir}
  pip install -r requirements.txt
  ```
* Setup database
  ```
  python manage.py migrate
  python manage.py makemigrations
  python manage.py migrate
  ```
* Set admin password in inital_setup.py and run it
  ```
  python initial_setup.py
  ```

If you have a list of recipes already then you can modify recipe_setup.py and update the user and recipes. Then run *python recipe_setup.py*

At this point you can start it and manage your recipes
```
python manage.py runserver <host>:<port>
``` 

### Change Password
Enter the url below and follow directions
```
https://{server}:{port}/accounts/password_change
```
When done navigate to the website https://{server}:{port}/foodmenu/recipes