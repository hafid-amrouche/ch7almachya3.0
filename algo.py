def algo():
    import json
    from product.models import ParentCategory, Category, Color, Document, Option, Fuel, GearBox
    from user.models import State

    f = open('data.json', encoding="utf8")

    data = json.load(f)


    for i in data:
        if i['model'] == "product.parentcategory" :
            ParentCategory.objects.create(
            name=i['fields']['name'],
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            slug=i['fields']['slug'],
            order=i['fields']['order'],
            icon=i['fields']['icon'],
            )
        
        
    for i in data:
        if i['model'] == "product.category" :
            category = Category.objects.create(
            name=i['fields']['name'],
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            slug=i['fields']['slug'],
            order=i['fields']['order'],
            icon=i['fields']['icon'],
            )
            if i['fields']['parent']:
                    category.parent = ParentCategory.objects.get(id = i['fields']['parent'])
                    category.save()

        elif i['model'] == "user.state" :
            State.objects.create(
            name=i['fields']['name'],
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            code=i['fields']['code'],
            order=i['fields']['order'],
            )

        elif i['model'] == "product.color" :
            Color.objects.create(
            name=i['fields']['name'],
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            )
        elif i['model'] == "product.document" :
            Document.objects.create(
            name=i['fields']['name'],
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            )
        elif i['model'] == "product.option" :
            Option.objects.create(
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            order=i['fields']['order'],
            )
        elif i['model'] == "product.fuel" :
            Fuel.objects.create(
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            )
        elif i['model'] == "product.gearbox" :
            GearBox.objects.create(
            name_ar=i['fields']['name_ar'],
            name_fr=i['fields']['name_fr'],
            name_en=i['fields']['name_en'],
            )
