import json
from collections import defaultdict
from datetime import datetime

# Загрузка данных из файла
with open('orders.json', 'r', encoding='utf-8') as f:
    orders = json.load(f)

# Инициализация переменных
max_price = 0
max_price_order_num = ''

max_quantity = 0
max_quantity_order_num = ''

orders_count_by_day = defaultdict(int)
user_orders_count = defaultdict(int)
user_total_spent = defaultdict(float)

total_orders_price = 0
total_orders_count = 0

total_items_price = 0
total_items_quantity = 0

# Обработка данных
for order_num, info in orders.items():
    date_str = info['date']
    user_id = info['user_id']
    quantity = info['quantity']
    price = info['price']

    # Самый дорогой заказ
    if price > max_price:
        max_price = price
        max_price_order_num = order_num

    # Заказ с максимальным количеством товаров
    if quantity > max_quantity:
        max_quantity = quantity
        max_quantity_order_num = order_num
        # Подсчет заказов по датам
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_str = date_obj.strftime('%Y-%m-%d')
            orders_count_by_day[day_str] += 1
        except ValueError:
            # Если дата некорректная, пропускаем
            print(f"Некорректная дата: {date_str} в заказе {order_num}")
            continue

    # Пользователь с наибольшим количеством заказов
    user_orders_count[user_id] += 1

    # Суммарная стоимость заказов по пользователю
    user_total_spent[user_id] += price

    # Общие суммы для средних
    total_orders_price += price
    total_orders_count += 1

    total_items_price += price
    total_items_quantity += quantity

# Ответы на вопросы
# 1. Самый дорогой заказ за июль
print(f"Номер самого дорого заказа: {max_price_order_num} на сумму {max_price}")

# 2. Заказ с самым большим количеством товаров
print(f"Номер заказа с максимальным количеством товаров: {max_quantity_order_num} на {max_quantity} товаров")

# 3. День с наибольшим количеством заказов
most_active_day = max(orders_count_by_day, key=orders_count_by_day.get)
print(f"День с наибольшим количеством заказов: {most_active_day} ({orders_count_by_day[most_active_day]} заказов)")

# 4. Пользователь, сделавший больше всего заказов
top_user_orders = max(user_orders_count, key=user_orders_count.get)
print(
    f"Пользователь с наибольшим количеством заказов: {top_user_orders} ({user_orders_count[top_user_orders]} заказов)")

# 5. Пользователь с наибольшей суммарной стоимостью заказов
top_user_spent = max(user_total_spent, key=user_total_spent.get)
print(f"Пользователь, потративший больше всего: {top_user_spent} на сумму {user_total_spent[top_user_spent]}")

# 6. Средняя стоимость заказа в июле
average_order_price = total_orders_price / total_orders_count if total_orders_count else 0
print(f"Средняя стоимость заказа: {average_order_price:.2f}")

# 7. Средняя стоимость товаров в июле
average_price_per_item = total_items_price / total_items_quantity if total_items_quantity else 0
print(f"Средняя стоимость товара: {average_price_per_item:.2f}")
