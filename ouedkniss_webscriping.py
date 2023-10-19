import json
#from django.utils.text import slugify

file_data = open('websrape_ouedkniss-master/data.json', encoding="utf-8")

file_data = json.load(file_data)['data']


#user = Account.objects.get(id=1)
  

left_cars = []
for key, announ in file_data.items() :
      if announ['priceType'] == "FIXED" :
            price = announ['pricePreview']
            given_price = 0

      elif announ['priceType'] == "OFFERED" :
            given_price = announ['pricePreview']
            price = 0

      else :
            price = 0
            given_price = 0

      is_all_options = False

      if announ['exchangeType'] == 'EXCHANGEABLE' :
            exchange = True
      else:
            exchange = False

      description = announ['description']

      for spec in announ['specs']:
            label = spec['specification']['label']
            if label == 'Year' :
                  year = int(spec['valueText'][0])
                  if year < 1900 and year > 2023 :
                        left_cars.append({announ['id'], 'year'})  
                        break 

            elif label == 'Energy':
                  fuel = spec['valueText'][0]

            elif label == 'Color':
                  color = spec['valueText'][0]

            elif label == 'Documents':
                  document = spec['valueText'][0]

            elif label == 'Engine':
                  engine = spec['valueText'][0]

            elif label == 'GearBox':
                  gear = spec['valueText'][0]


            elif label == 'Car Options':
                  options_list = spec['valueText']
            
            elif label == "mileage":
                  distance = int(spec['value'][0])

            elif label == "Model":
                  name = spec['valueText']
                  # slug = slugif(name)

            
      print(name)
