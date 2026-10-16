from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Restaurant, FoodItem, Category

def home(request):
    restaurants = Restaurant.objects.all().order_by("name")
    categories = Category.objects.all().order_by("name")
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    if query:
        restaurants = restaurants.filter(name__icontains=query) | restaurants.filter(cuisine__icontains=query)
    if category_id.isdigit():
        restaurants = restaurants.filter(menu_items__category_id=int(category_id)).distinct()
    return render(request, "restaurants/home.html", {
        "restaurants": restaurants.distinct(), "categories": categories,
        "query": query, "selected_category": category_id,
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_items = restaurant.menu_items.filter(is_available=True).select_related("category").order_by("category__name", "name")
    categories = Category.objects.all().order_by("name")
    category_id = request.GET.get("category", "").strip()
    if category_id.isdigit():
        menu_items = menu_items.filter(category_id=int(category_id))
    return render(request, "restaurants/restaurant_detail.html", {
        "restaurant": restaurant, "menu_items": menu_items, "categories": categories,
        "selected_category": category_id,
    })

def food_detail(request, food_id):
    food = get_object_or_404(FoodItem.objects.select_related("restaurant", "category"), pk=food_id)
    return render(request, "restaurants/food_detail.html", {"food": food})

def cart_data(request):
    cart = request.session.get("cart", {})
    items, total, count = [], 0, 0
    for food_id, qty in cart.items():
        try:
            food = FoodItem.objects.get(pk=int(food_id), is_available=True)
            qty = max(1, int(qty))
        except (FoodItem.DoesNotExist, ValueError, TypeError):
            continue
        subtotal = food.price * qty
        items.append({"food": food, "quantity": qty, "subtotal": subtotal})
        total += subtotal
        count += qty
    return items, total, count

@require_POST
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id, is_available=True)
    cart = request.session.get("cart", {})
    key = str(food.id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.POST.get("next") or "cart")

def cart_view(request):
    items, total, count = cart_data(request)
    return render(request, "restaurants/cart.html", {"items": items, "total": total, "count": count})

@require_POST
def update_cart(request, food_id):
    cart = request.session.get("cart", {})
    key, action = str(food_id), request.POST.get("action")
    if key in cart:
        if action == "increase":
            cart[key] = int(cart[key]) + 1
        elif action == "decrease":
            cart[key] = int(cart[key]) - 1
            if cart[key] <= 0:
                cart.pop(key, None)
        elif action == "remove":
            cart.pop(key, None)
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")

@require_POST
def clear_cart(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart")
