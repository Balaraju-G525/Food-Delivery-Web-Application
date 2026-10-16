from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, Category, FoodItem


class Command(BaseCommand):
    help = "Create sample restaurants, categories, and menu items."

    def handle(self, *args, **options):
        categories = {}
        for name in ["Biryani", "Pizza", "Burgers", "South Indian", "Desserts"]:
            categories[name], _ = Category.objects.get_or_create(name=name)

        samples = [
            {
                "name": "Spice Garden",
                "description": "Comforting Indian meals made fresh to order.",
                "cuisine": "Indian",
                "location": "Kadapa",
                "items": [
                    ("Chicken Biryani", "Aromatic rice with spiced chicken.", "189.00", "Biryani", False),
                    ("Veg Biryani", "Fragrant basmati rice with vegetables.", "139.00", "Biryani", True),
                    ("Gulab Jamun", "Soft milk dumplings in syrup.", "69.00", "Desserts", True),
                ],
            },
            {
                "name": "Crust & Cheese",
                "description": "Pizza favourites with a crispy crust.",
                "cuisine": "Italian",
                "location": "Kadapa",
                "items": [
                    ("Margherita Pizza", "Classic tomato, cheese, and basil.", "179.00", "Pizza", True),
                    ("Veggie Burger", "A crunchy vegetable patty with fresh toppings.", "119.00", "Burgers", True),
                ],
            },
            {
                "name": "Tiffin Corner",
                "description": "South Indian breakfast and evening snacks.",
                "cuisine": "South Indian",
                "location": "Kadapa",
                "items": [
                    ("Masala Dosa", "Crisp dosa with potato masala.", "89.00", "South Indian", True),
                    ("Idli (2 pieces)", "Steamed idlis served with chutney.", "49.00", "South Indian", True),
                ],
            },
        ]


        # Twenty additional demo menu items
        extra_items = [
            ("Paneer Butter Masala", "Creamy tomato gravy with paneer.", "179.00", "Biryani", True, "Spice Garden"),
            ("Chicken 65", "Crispy spicy chicken bites.", "169.00", "Biryani", False, "Spice Garden"),
            ("Egg Fried Rice", "Wok-tossed rice with egg and vegetables.", "129.00", "South Indian", False, "Spice Garden"),
            ("Mushroom Biryani", "Basmati rice cooked with mushrooms.", "149.00", "Biryani", True, "Spice Garden"),
            ("Double Ka Meetha", "Traditional bread pudding dessert.", "79.00", "Desserts", True, "Spice Garden"),
            ("Pepper Chicken", "Chicken tossed with cracked pepper.", "189.00", "Biryani", False, "Spice Garden"),
            ("Paneer Tikka Pizza", "Pizza topped with paneer tikka.", "229.00", "Pizza", True, "Crust & Cheese"),
            ("Farmhouse Pizza", "Bell peppers, onion, corn, and cheese.", "249.00", "Pizza", True, "Crust & Cheese"),
            ("BBQ Chicken Pizza", "Smoky barbecue chicken and cheese.", "279.00", "Pizza", False, "Crust & Cheese"),
            ("Garlic Bread", "Toasted bread with garlic butter.", "99.00", "Pizza", True, "Crust & Cheese"),
            ("Classic Cheese Burger", "Burger with cheese and lettuce.", "149.00", "Burgers", True, "Crust & Cheese"),
            ("Crispy Chicken Burger", "Crispy chicken with house sauce.", "179.00", "Burgers", False, "Crust & Cheese"),
            ("French Fries", "Golden, lightly salted fries.", "89.00", "Burgers", True, "Crust & Cheese"),
            ("Chocolate Brownie", "Rich chocolate brownie.", "89.00", "Desserts", True, "Crust & Cheese"),
            ("Plain Dosa", "Crispy golden dosa with chutney.", "69.00", "South Indian", True, "Tiffin Corner"),
            ("Onion Uttapam", "Soft uttapam topped with onion.", "79.00", "South Indian", True, "Tiffin Corner"),
            ("Medu Vada", "Crispy lentil doughnuts with chutney.", "55.00", "South Indian", True, "Tiffin Corner"),
            ("Pongal", "Rice and lentils with mild spices.", "69.00", "South Indian", True, "Tiffin Corner"),
            ("Filter Coffee", "South Indian filter coffee.", "35.00", "Desserts", True, "Tiffin Corner"),
            ("Kesari Bath", "Sweet semolina dessert with ghee.", "59.00", "Desserts", True, "Tiffin Corner"),
        ]
        restaurant_by_name = {r.name: r for r in Restaurant.objects.all()}
        for name, description, price, category_name, vegetarian, restaurant_name in extra_items:
            restaurant = restaurant_by_name.get(restaurant_name)
            if restaurant:
                FoodItem.objects.get_or_create(
                    restaurant=restaurant, name=name,
                    defaults={"description": description, "price": price,
                              "category": categories[category_name], "is_vegetarian": vegetarian},
                )

        for data in samples:
            restaurant, _ = Restaurant.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "cuisine": data["cuisine"],
                    "location": data["location"],
                },
            )
            for name, description, price, category_name, vegetarian in data["items"]:
                FoodItem.objects.get_or_create(
                    restaurant=restaurant,
                    name=name,
                    defaults={
                        "description": description,
                        "price": price,
                        "category": categories[category_name],
                        "is_vegetarian": vegetarian,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Sample food delivery data added successfully."))
