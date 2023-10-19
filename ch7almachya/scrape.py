import requests
import json
import datetime
from django.http import HttpResponse
from dashboard.views import create_item_OK
from ch7almachya.settings import BASE_DIR
import os

def get_cars(Query,req_pages):
    global url
    url= "https://api.ouedkniss.com/graphql"
    payload = json.dumps({
        "operationName": "SearchQuery",
        "variables": {
            "mediaSize": "MEDIUM",
            "q": Query,
            "filter": {
                "categorySlug": "automobiles",
                "origin": None,
                "connected": False,
                "delivery": None,
                "regionIds": [],
                "cityIds": [],
                "priceRange": [
                    None,
                    None
                ],
                "exchange": False,
                "hasPictures": False,
                "hasPrice": False,
                "priceUnit": None,
                "fields": [],
                "page": 1,
                "count": 48
            }
        },
        "query": "query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  __typename\n}\n"
    })
    headers = {
        'authority': 'api.ouedkniss.com',
        'accept': '*/*',
        'accept-language': 'en',
        'authorization': '',
        'content-type': 'application/json',
        'dnt': '1',
        'locale': 'en',
        'origin': 'https://www.ouedkniss.com',
        'referer': 'https://www.ouedkniss.com/',
        'save-data': 'on',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'x-app-version': '"2.1.27"',
        'x-referer': 'https://www.ouedkniss.com/automobiles/1?keywords=208',
        'x-track-id': '23efcadb-f886-44b1-93ce-97f7ed21dd07',
        'x-track-timestamp': '1688507964'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    maxpage = response.json()['data']['search']['announcements']['paginatorInfo']['lastPage']
    print(maxpage)
    cars = []
    Pages = min(int(req_pages), int(maxpage))
    print(f"pages that are going to be checked are {Pages}")
    for page in range(1,Pages+1):
        print(f"Getting page {page}!")
        payload = json.dumps({
            "operationName": "SearchQuery",
            "variables": {
                "mediaSize": "MEDIUM",
                "q": Query,
                "filter": {
                    "categorySlug": "automobiles",
                    "origin": None,
                    "connected": False,
                    "delivery": None,
                    "regionIds": [],
                    "cityIds": [],
                    "priceRange": [
                        None,
                        None
                    ],
                    "exchange": False,
                    "hasPictures": False,
                    "hasPrice": False,
                    "priceUnit": None,
                    "fields": [],
                    "page": page,
                    "count":48
                }
            },
            "query": "query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  __typename\n}\n"
        })
        headers = {
            'authority': 'api.ouedkniss.com',
            'accept': '*/*',
            'accept-language': 'en',
            'authorization': '',
            'content-type': 'application/json',
            'dnt': '1',
            'locale': 'en',
            'origin': 'https://www.ouedkniss.com',
            'referer': 'https://www.ouedkniss.com/',
            'save-data': 'on',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
            'x-app-version': '"2.1.27"',
            'x-referer': 'https://www.ouedkniss.com/automobiles/1?keywords=208',
            'x-track-id': '23efcadb-f886-44b1-93ce-97f7ed21dd07',
            'x-track-timestamp': '1688507964'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        cars.append(response.json()['data']['search']['announcements']['data'])
    return cars

print(datetime.datetime.now())

def scrape(request):
    if request.user.id == 1 :
        cars = get_cars(request.GET.get('key'),int(request.GET.get('pages')))
        cars_data = []
        for page in cars:
            for car in page:
                payload = json.dumps({
                    "operationName": "AnnouncementGet",
                    "variables": {
                        "id": car['id']
                    },
                    "query": "query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    oldPricePreview\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      id\n      slug\n      name\n      deliveryType\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      announcementsCount\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      pricePreview\n      oldPricePreview\n      quantity\n      __typename\n    }\n    showAnalytics\n    __typename\n  }\n}\n"
                })
                headers = {
                    'authority': 'api.ouedkniss.com',
                    'accept': '*/*',
                    'accept-language': 'en',
                    'authorization': '',
                    'content-type': 'application/json',
                    'dnt': '1',
                    'locale': 'en',
                    'origin': 'https://www.ouedkniss.com',
                    'referer': 'https://www.ouedkniss.com/',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
                    'x-app-version': '"2.1.27"',
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(f"processing car id: {car['id']}")
                car_data = json.loads(response.text)
                file_data = open(os.path.join(BASE_DIR, 'webscrape_ouedkniss-master/data.json'), encoding="utf-8")
                file_data = json.load(file_data)
                file_data['data']['announcement_' + str(car['id'])] = car_data['data']['announcement']

                with open(os.path.join(BASE_DIR, 'webscrape_ouedkniss-master/data.json')  , 'w') as f:
                    json.dump(file_data, f)
                cars_data.append(response.text)
        print(datetime.datetime.now())

        return HttpResponse('')




