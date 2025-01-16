from collections import deque
from typing import Any, Dict, List, Union

def check_for_null_values(
    json_data: Union[Dict, List], 
    optional_paths: List[str] = None
):
    """
    This function checks a JSON structure to identify fields that contain null (None) values.
    Any fields with None values will be reported unless they are in the 'optional_paths'.

    :param json_data: The JSON data (dictionary or list) to validate.
    :param optional_paths: A list of field paths to ignore. Fields in this list can have None values.
    :return: A dictionary with a status ('success' or 'error') and a list of problematic paths.
    """
    if optional_paths is None:
        optional_paths = []
    
    items_to_check = deque([(json_data, "")])
    
    invalid_fields = []
    
    while items_to_check:
        current_item, current_path = items_to_check.popleft()
        
        if isinstance(current_item, dict):
            for key, value in current_item.items():
                path = f"{current_path}.{key}" if current_path else key
                if value is None and path not in optional_paths:
                    invalid_fields.append(path)
                elif isinstance(value, (dict, list)):
                    items_to_check.append((value, path))
        
        elif isinstance(current_item, list):
            for index, element in enumerate(current_item):
                path = f"{current_path}[{index}]"
                if element is None and path not in optional_paths:
                    invalid_fields.append(path)
                elif isinstance(element, (dict, list)):
                    items_to_check.append((element, path))

    if invalid_fields:
        return {"status": "error", "invalid_fields": invalid_fields}
    
    return {"status": "success"}


valid_example = {
  "user": {
    "id": 12345,
    "username": "alice123",
    "email": "alice@example.com",
    "profile": {
      "first_name": "Alice",
      "last_name": "Doe",
      "age": 30,
      "address": {
        "street": "123 Main St",
        "city": "Seattle",
        "zipcode": "98101"
      },
      "preferences": {
        "language": "English",
        "notifications": True
      }
    },
    "friends": [
      {
        "user_id": 67890,
        "username": "bob234",
        "email": "bob@example.com",
        "profile": {
          "first_name": "Bob",
          "last_name": "Smith",
          "age": 35,
          "address": {
            "street": "456 Oak Rd",
            "city": "Portland",
            "zipcode": "97201"
          }
        }
      },
      {
        "user_id": 11223,
        "username": "charlie456",
        "email": "charlie@example.com",
        "profile": {
          "first_name": "Charlie",
          "last_name": "Brown",
          "age": 25,
          "address": {
            "street": "789 Pine Ave",
            "city": "Seattle",
            "zipcode": "98102"
          }
        }
      }
    ]
  },
  "orders": [
    {
      "order_id": "A1234",
      "items": [
        {
          "product": "Laptop",
          "price": 1200,
          "quantity": 1
        },
        {
          "product": "Mouse",
          "price": 25,
          "quantity": 1
        }
      ],
      "status": "shipped"
    },
    {
      "order_id": "A5678",
      "items": [
        {
          "product": "Tablet",
          "price": 500,
          "quantity": 2
        },
        {
          "product": "Headphones",
          "price": 50,
          "quantity": 1
        }
      ],
      "status": "delivered"
    }
  ]
}

# Example of invalid JSON data
invalid_example = {
  "user": {
    "id": 12345,
    "username": "alice123",
    "email": "alice@example.com",
    "profile": {
      "first_name": "Alice",
      "last_name": "Doe",
      "age": None,
      "address": {
        "street": "123 Main St",
        "city": None,
        "zipcode": "98101"
      },
      "preferences": {
        "language": "English",
        "notifications": True
      }
    },
    "friends": [
      {
        "user_id": 67890,
        "username": "bob234",
        "email": "bob@example.com",
        "profile": {
          "first_name": "Bob",
          "last_name": "Smith",
          "age": 35,
          "address": {
            "street": "456 Oak Rd",
            "city": "Portland",
            "zipcode": "97201"
          }
        }
      },
      {
        "user_id": 11223,
        "username": "charlie456",
        "email": "charlie@example.com",
        "profile": {
          "first_name": "Charlie",
          "last_name": "Brown",
          "age": None,
          "address": {
            "street": "789 Pine Ave",
            "city": "Seattle",
            "zipcode": None
          }
        }
      }
    ]
  },
  "orders": [
    {
      "order_id": "A1234",
      "items": [
        {
          "product": "Laptop",
          "price": 1200,
          "quantity": 1
        },
        {
          "product": "Mouse",
          "price": 25,
          "quantity": 1
        }
      ],
      "status": "shipped"
    },
    {
      "order_id": "A5678",
      "items": [
        {
          "product": "Tablet",
          "price": 500,
          "quantity": 2
        },
        {
          "product": "Headphones",
          "price": 50,
          "quantity": 1
        }
      ],
      "status": "delivered"
    }
  ]
}


optional_paths = [
    "user.profile.address.city",
    "user.friends[1].profile.address.zipcode"
]


print(check_for_null_values(valid_example, optional_paths))
print(check_for_null_values(invalid_example, optional_paths))  