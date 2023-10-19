states = State.objects.all()
accounts = Account.objects.all()
categories = Category.objects.all()
colors = Color.objects.all()
documents = Document.objects.all()
fuels = Fuel.objects.all()
gearboxs = GearBox.objects.all()
all_options_list = Option.objects.all()
for i in range(1000):
    n = random.randint(0, 14)
    state = random.choice(states)
    user = random.choice(accounts)
    brand = random.choice(categories)
    name = random.choice('abcdefghijklmnopqrstuvwxyz') + random.choice('abcdefghijklmnopqrstuvwxyz') + random.choice('abcdefghijklmnopqrstuvwxyz') + random.choice('abcdefghijklmnopqrstuvwxyz')
    year = random.choice(range(1950, 2022))
    color = random.choice(colors)
    document = random.choice(documents)
    price = random.choice([None] + list(range(40, 1500)))
    given_price = random.choice([None] + list(range(40, 1500)))
    distance = random.choice(range(0, 1000))
    fuel = random.choice(fuels)
    gear_box = random.choice(gearboxs)
    exchange = random.choice([True, False])
    is_all_options = random.choice([True, False])
    used = random.choice([True, False])
    image = ""
    product = Product.objects.create(
            state = state,
            user = user,
            category = brand,
            name= name,
            year = year,
            color = color,
            document = document,
            price = price,
            given_price = given_price,
            destance = distance,
            fuel = fuel,
            gear_box = gear_box,
            exchange = exchange,
            is_all_options = is_all_options,
            image= image,
            city = "bougara",
            phone_number="0541356564"
    )
    options_list = []
    for i in range(n):
        option = random.choice(all_options_list)
        product.options.add(option)
        options_list.append(option.id)
    product.options_list = json.dumps(list(set(options_list)))
    product.save()
