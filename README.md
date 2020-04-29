# Restaurant Reservation Service
This porject is for my final project of FSND of Udaicty. It provides reservation service for customers and owners. Customers can search restaurants and make a reservation. Owners can post thier restaurant and check their reservation thourgh this service.

There are 3 roles: Admin, Customer, Owner. 
Admin can access every endpoint and only admin can delete data. Customer can only access to the endpoints which are about customers and their reservations. Owners can only access to the endpoints which are about restaurants. Here's the details.

## Admin
- check:reservations
- delete:customer
- delete:restaurant
- edit:customer
- edit:reservation
- edit:restaurant
- get:customers
- get:reservations
- get:restaurant
- get:restaurants
- make:reservation
- post:customer
- post:restaurants
- post:review
- search:restaurants

## Customer
- edit:customer
- edit:reservation
- get:reservations
- get:restaurant
- get:restaurants
- make:reservation
- post:customer
- post:review
- search:restaurants

## Owner
- check:reservations
- edit:restaurant
- get:restaurants
- post:restaurants

All backend code follows PEP8 style guidelines.

# Getting Started
The application is run on https://capstone-reservation-service.herokuapp.com/ by default.

This application only has backend except the index page. At the index page, you can login as a specific role. After you logged in, use the token as a header.


# API Reference
- Base URL: https://capstone-reservation-service.herokuapp.com/
- Authentication: This project used Third-Party Authentication with Auth0. Please use the token out of the URL after you logged in and add it to 'Authentication: Bearer YOUR_TOKEN' as a header.


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
  'success': False,
  'maessage': 'Not Processable',
  'error': 422
}
```
The API will return four error types when requests fail:
- 401: Authentification Fails
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed

## Endpoints

### Restaurants
---
### GET /restaurants
- General:
  - Returns a list of restaurant objects, success value, and total number of restaurants.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1(default).
- Required Permission: 'get:restaurants'. All of the roles can access to this endpoint.
- Sample:
```
curl --request GET \
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "restaurants": [
        {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 1,
            "name": "Saiwalks",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        },
        {
            "address": "420 Geary St, San Francisco, CA 94102",
            "category": "Thai",
            "id": 2,
            "name": "The Thonglor",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/Q7CsR9r7ATt1Om9FvrJbTw/o.jpg",
            "tel": "415-346-3121"
        },
        {
            "address": "Pier 39, Ste A-202, San Francisco, CA 94133",
            "category": "Seafood",
            "id": 3,
            "name": "Fog Harbor Fish House",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/vLglztGWU-rhuAhDyp1LCQ/o.jpg",
            "tel": "415-421-2442"
        }
    ],
    "success": true,
    "total_restaurants": 3
}
```


### POST /restaurants/create
- General:
  - Creates a new restaurant using the submitted data. Returns id of the created restaurant, current restaurants list, success value and total number of restuarnats. 
- Required Permission: 'post:restaurants'. Admin and Owner can access to this endpoint.
- Sample:
```
curl --request POST \
  --data '{"name": "Howlin' Ray's", "address":"727 N Broadway, Ste 128, Los Angeles, CA 90012","category":"American","photo":"https://s3-media0.fl.yelpcdn.com/bphoto/0I7JC7Vp8hBrwQMloYuDkQ/o.jpg","tel": "213-935-8399", "menu":"{Fried Chicken, Hot Chicken, Chicken Sando}","capacity":"20","open_time":"11:00:00", "close_time":"19:00:00"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants/create'\
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "created": 7,
    "current_restaurants": [
        {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 1,
            "name": "Saiwalks",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        },
        {
            "address": "420 Geary St, San Francisco, CA 94102",
            "category": "Thai",
            "id": 2,
            "name": "The Thonglor",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/Q7CsR9r7ATt1Om9FvrJbTw/o.jpg",
            "tel": "415-346-3121"
        },
        {
            "address": "Pier 39, Ste A-202, San Francisco, CA 94133",
            "category": "Seafood",
            "id": 3,
            "name": "Fog Harbor Fish House",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/vLglztGWU-rhuAhDyp1LCQ/o.jpg",
            "tel": "415-421-2442"
        },
        {
            "address": "727 N Broadway, Ste 128, Los Angeles, CA 90012",
            "category": "American",
            "id": 7,
            "name": "Howlin' Ray's",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/0I7JC7Vp8hBrwQMloYuDkQ/o.jpg",
            "tel": "213-935-8399"
        }
    ],
    "success": true,
    "total_restaurants": 4
}
```


### POST /restaurants/search
- Parameter
  - searchTerm(Required): The keyword of the restaurant name which you want to find.
- General:
  - Search restaurants using the searchTerm parameter. Returns success value, searched restaruants list and numbers of them.
- Required Permission: 'search:restaurants'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request POST \
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants/search?searchTerm=fish' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "current_restaurants": [
        {
            "address": "Pier 39, Ste A-202, San Francisco, CA 94133",
            "category": "Seafood",
            "id": 3,
            "name": "Fog Harbor Fish House",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/vLglztGWU-rhuAhDyp1LCQ/o.jpg",
            "tel": "415-421-2442"
        }
    ],
    "success": true,
    "total_restaurants": 1
}
```

### GET /restaurants/{restaurant_id}
- General:
  - Returns success value, resturant id and information of the restaurant.
- Required Permission: 'get:restaurant'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request GET \
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants/1' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample:
```
{
    "rest_id": 1,
    "restaurant": {
        "address": "3348 Steiner St, San Francisco, CA 94123",
        "category": "Vietnamese",
        "id": 1,
        "name": "Saiwalks",
        "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
        "tel": "415-549-7932"
    },
    "success": true
}
```


### DELETE /restaurants/{restaurant_id}
- General:
  - Delete a restaurant. Returns success value, id of deleted restaurant, list of current restuarants and total number of restaurants.
- Required Permission: 'delete:restaurant'. Only Admin can access to this endpoint.
- Sample:
```
curl --request DELETE \
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants/7' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "current_restaurants": [
        {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 1,
            "name": "Saiwalks",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        },
        {
            "address": "420 Geary St, San Francisco, CA 94102",
            "category": "Thai",
            "id": 2,
            "name": "The Thonglor",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/Q7CsR9r7ATt1Om9FvrJbTw/o.jpg",
            "tel": "415-346-3121"
        },
        {
            "address": "Pier 39, Ste A-202, San Francisco, CA 94133",
            "category": "Seafood",
            "id": 3,
            "name": "Fog Harbor Fish House",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/vLglztGWU-rhuAhDyp1LCQ/o.jpg",
            "tel": "415-421-2442"
        }
    ],
    "deleted": 7,
    "success": true,
    "total_restaurants": 3
}
```

### PATCH /restaurants/{restaurant_id}/edit
- General:
  - Edit a restaurant. Returns success value, id of edited restaurant and list of current restuarants.
- Required Permission: 'edit:restaurant'. Admin and Owner can access to this endpoint.
- Sample:
```
curl --request PATCH \
  --data '{"name": "The Thonglor", "address":"3348 Steiner St, San Francisco, CA 94123","category":"Vietnamese","photo":"https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg","tel": "415-549-7932", "menu":"{Pho Ga,Pho Bo,Pho Comfort Chicken}","capacity":"10","open_time":"10:00:00", "close_time":"22:00:00"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/restaurants/2/edit' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "current_restaurants": [
        {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 1,
            "name": "Saiwalks",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        },
        {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 2,
            "name": "The Thonglor",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        },
        {
            "address": "Pier 39, Ste A-202, San Francisco, CA 94133",
            "category": "Seafood",
            "id": 3,
            "name": "Fog Harbor Fish House",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/vLglztGWU-rhuAhDyp1LCQ/o.jpg",
            "tel": "415-421-2442"
        }
    ],
    "edited": 2,
    "success": true
}
```
<br>

### Customers
---
### GET /customers
- General:
  - Returns success value, total number of customers and list of current customers with their information. It's only for admin because of privacy issue.
- Required Permission: 'get:customers'. Only Admin can access to this endpoint.
- Sample:
```
curl --request GET \
  --url 'https://capstone-reservation-service.herokuapp.com/customers' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "current_customers": [
        {
            "email": "kelly@email.com",
            "id": 2,
            "name": "Kelly",
            "phone": "213-222-2413"
        },
        {
            "email": "lang@eamil.com",
            "id": 3,
            "name": "Lang",
            "phone": "929-332-6403"
        },
        {
            "email": "hazzel@eamil.com",
            "id": 1,
            "name": "Hazzel",
            "phone": "241-343-6116"
        },
        {
            "email": "imjenny@email.com",
            "id": 4,
            "name": "Jenny",
            "phone": "623-151-1421"
        }
    ],
    "success": true,
    "total_customers": 4
}
```

### POST /customers/create
- General:
  - Creates a new customer using the submitted data. Returns success value and information of the user.
- Required Permission: 'post:customer'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request POST \
  --data '{"name": "Jenny", "phone": "623-151-1421", "email":"imjenny@email.com"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/customers/create' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample:
```
{
    "customer": {
        "email": "imjenny@email.com",
        "id": 7,
        "name": "Jenny",
        "phone": "623-151-1421"
    },
    "success": true
}
```


### POST /restaurants/{customer_id}/edit
- General:
  - Edit a customer. Returns customer's data and success value.
- Required Permission: 'edit:customer'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request POST \
  --data '{"name": "Jenny Liu", "phone": "253-132-1111", "email":"imjenny@email.com"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/customers/4/edit' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "customer": {
        "email": "imjenny@email.com",
        "id": 7,
        "name": "Jenny Liu",
        "phone": "253-132-1111"
    },
    "success": true
}
```

### DELETE /customers/{customer_id}
- General:
  - Delete a customer. Returns success value and id of deleted customer.
- Required Permission: 'delete:customer'. Only Admin can access to this endpoint.
- Sample:
curl --request DELETE \
  --url 'https://capstone-reservation-service.herokuapp.com/customers/4' \
  --header 'Authorization: Bearer YOUR_TOKEN'
- Response Sample
```
{
    "deleted": 7,
    "success": true
}
```

<br>

### Reservations
---

### POST /reservations/create
- Parameters
  - customer_eamil(Required): Email of customer who want to make reservation.
  - rest_name(Required): Name of restaurant which will be reserved.
  - If your reservation is over the capacity of a restaurant the reservation cannot succeed.
- General:
  - Creates a new reservation using the submitted data. Returns success value and details of the reservation with information of customer and restaurant.
- Required Permission: 'make:reservation'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request POST \
  --data '{"time":"2021-01-10 12:00:00", "number":"3"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/reservations/create?customer_email=lang@eamil.com&rest_name=The Thonglor' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "reservation": {
        "customer": {
            "email": "lang@eamil.com",
            "id": 3,
            "name": "Lang",
            "phone": "929-332-6403"
        },
        "reservation": {
            "customer_id": 3,
            "id": 9,
            "number": 3,
            "request": null,
            "rest_id": 2,
            "review": null,
            "time": "Sun, 10 Jan 2021 12:00:00 GMT"
        },
        "restaurant": {
            "address": "3348 Steiner St, San Francisco, CA 94123",
            "category": "Vietnamese",
            "id": 2,
            "name": "The Thonglor",
            "photo": "https://s3-media0.fl.yelpcdn.com/bphoto/hJ_qCH6m8umt3z5-xPZReA/o.jpg",
            "tel": "415-549-7932"
        }
    },
    "success": true
}
```

### GET /reservations/{customer_id}
- General:
  - Customers can check their past and upcoming reservations. Returns success value and details of reservations.
- Required Permission: 'get:reservations'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request GET \
  --url 'https://capstone-reservation-service.herokuapp.com/reservations/1' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "past_reservations": [
        {
            "customer_id": 1,
            "id": 1,
            "number": 3,
            "request": "Party Room",
            "rest_id": 1,
            "review": "That was perpact party!",
            "time": "Thu, 15 Aug 2019 17:00:00 GMT"
        }
    ],
    "success": true,
    "upcoming_reservations": [
        {
            "customer_id": 1,
            "id": 2,
            "number": 4,
            "request": "Baby Seat",
            "rest_id": 1,
            "review": null,
            "time": "Sat, 15 Aug 2020 17:00:00 GMT"
        }
    ]
}
```

### GET /reservations/{restaurant_id}/owner
- General:
  - Owners can check past and upcoming reservations of thier restaurant. Returns success value and details of reservations.
- Required Permission: 'check:reservations'. Admin and Owner can access to this endpoint.
- Sample:
```
curl --request GET \
  --url 'https://capstone-reservation-service.herokuapp.com/reservations/2/owner' \
  --header 'Authorization: Bearer YOUR_TOKEN'
``` 
- Response Sample
```
{
    "past_reservations": [],
    "success": true,
    "upcoming_reservations": [
        {
            "customer": {
                "email": "lang@eamil.com",
                "id": 3,
                "name": "Lang",
                "phone": "929-332-6403"
            },
            "reservations": {
                "customer_id": 3,
                "id": 3,
                "number": 2,
                "request": null,
                "rest_id": 2,
                "review": null,
                "time": "Wed, 13 May 2020 12:00:00 GMT"
            }
        },
        {
            "customer": {
                "email": "lang@eamil.com",
                "id": 3,
                "name": "Lang",
                "phone": "929-332-6403"
            },
            "reservations": {
                "customer_id": 3,
                "id": 9,
                "number": 3,
                "request": null,
                "rest_id": 2,
                "review": null,
                "time": "Sun, 10 Jan 2021 12:00:00 GMT"
            }
        }
    ]
}
```

### PATCH /reservations/{reservation_id}/review
- General:
  - Customers can leave a review how was their experience about past reservation. Returns success value and details of reservations with the new review.
- Required Permission: 'post:review'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request PATCH \
  --data '{"review":"Excellent! I'll come again with my family."}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/reservations/1/review' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "reservation": {
        "customer_id": 1,
        "id": 1,
        "number": 3,
        "request": "Party Room",
        "rest_id": 1,
        "review": "Excellent! I'll come again with my family.",
        "time": "Thu, 15 Aug 2019 17:00:00 GMT"
    },
    "success": true
}
```

### PATCH /reservations/{reservation_id}/edit
- General:
  - Customers can edit their reservation. Returns success value and details of reservations.
- Required Permission: 'edit:review'. Admin and Customer can access to this endpoint.
- Sample:
```
curl --request PATCH \
  --data '{"time":"2020-08-14 17:00:00", "number":"5", "request": "One Baby Seat"}'\
  --header "Content-Type: application/json"\
  --url 'https://capstone-reservation-service.herokuapp.com/reservations/2/edit' \
  --header 'Authorization: Bearer YOUR_TOKEN'
```
- Response Sample
```
{
    "reservation": {
        "customer_id": 1,
        "id": 2,
        "number": 5,
        "request": "One Baby Seat",
        "rest_id": 1,
        "review": null,
        "time": "Fri, 14 Aug 2020 17:00:00 GMT"
    },
    "success": true
}
```
# Authors
Hyunlang Ban

