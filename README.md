# Food Delivery Web Application

A beginner-friendly food browsing app built with Python and Django. It includes restaurant listings, food categories, menu items, search, and item detail pages.

## Requirements
- Python 3.10+
- pip

## Run on macOS
Open Terminal and move into this folder:

```bash
cd food_delivery_web_application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_food
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Pages
- `/` — restaurant listings
- `/restaurant/<id>/` — restaurant menu
- `/food/<id>/` — food item details

## Notes
This is a learning/demo project. It does not process real orders or payments. Menu and restaurant data are demo data created by the `seed_food` command.
