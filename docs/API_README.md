## API Docs

## REST API
### Interface to send application
To start to use the application user should apply for it and face with application administrator control.

| URI             | Method  | Authorization |
|-----------------|---------|---------------|
|`api/v1/apply/`  | `POST`  | not required  |

Param: json data
```
{
  "code": [string],  # the user id in the social platform
  "first_name": [string],
  "last_name": [string]
}
```

Success Response:
* Code: 201

Error Response:
* Code: 400
* How to solve:
    - check that your request provide correct param data
    - check user status, there is a probability that user already have applied
    
### Interface to obtain signature for vk app user
When vk app is first time launched the request with parameters to check signature is sent.
Client should redirect the request to the server to obtain social user signature.

| URI               | Method  | Authorization |
|-------------------|---------|---------------|
|`api/v1/vk_auth/`  | `GET`   | not required  |

Success Response:
* Code: 200
* Body:

    ```
    {
      "password": [string]
    }
    ```

Error Response:
* Code: 400
* How to solve: provide valid parameters.

* Code: 401
* How to solve: just wait until admin associate your social user with system one.

* Code: 403
* How to solve: send request to [apply to join](interface-to-send-application).


## GraphQL API
Notes: 
- GraphQL API always return 200 status code even if contain errors. You need to check the response body.
- All mutations are POST requests and queries - GET ones.

### Interface to obtain tokens

```
mutation tokenAuth {
  tokenAuth(username: "username", password: "password") {
    token
    refreshToken
    refreshExpiresIn
    payload
  }
}
```
If you need to obtain tokens for social user pass social user id as `username` and
signature obtained on the [previous step](interface-to-obtain-signature-for-vk-app-user) 
as `password`.

To send authorized request you should set the `Authorization` header:

```
POST / HTTP/1.1
Host: some_host.com
Authorization: JWT <token>
Content-Type: application/json;
```

### Gifts API
Gifts are attached to the specific hero class.
Gifts can be personal and group-wide. Group gift is available if it can be bought by 
the student with the smallest coins quantity in the learning group.

#### availableGifts

##### Return available gifts for the student

| Type    | User type     | Authorization |
|--------|---------------|---------------|
| query | student only  | required      |

Arguments:
* `isGroupWide` - optional boolean argument, use it to filtrate output

Schema:
```
query availableGifts {
    availableGifts {
        name
        price
        isGroupWide
        remain
        canBuy
    }
}
```
---
##### Return available personal gifts for the specified student user

| Type    | User type      | Authorization |
|--------|-----------------|---------------|
| query | staff users only | required      |

Arguments:
* `userId` - id of the student
* `isGroupWide` - optional boolean argument, use it to filtrate output

Schema:

```
query availableGifts($userId:Int!){
    availableGifts(userId: $userId) {
        name
        price
        isGroupWide
        remain
        canBuy
    }
}
```

##### Buy or use gift 

| Type       | User type      | Authorization |
|-----------|-----------------|---------------|
| mutation | student only     | required      |

Arguments:
* `giftClassId` - id of the available gift
* `quantity` - positive number for buying, negative - for using gift

Schema:

```
mutation BuyOrUseUserGiftMutation($giftClassId:Int!, $quantity:Float!) {
    buyOrUseGift(giftClassId: $giftClassId, quantity: $quantity) {
        userGift {
            id
        }
    }
}
```

##### Return user's hero backpack

| Type    | User type      | Authorization |
|--------|-----------------|---------------|
| query | student only     | required      |


Schema:

```
query HeroBackpack {
    heroBackpack {
        giftClassName
        quantity
        datetimeEdited
        datetimeCreated
    }
}
```

### Teacher Dashboard API

##### Get list of the learning groups

| Type    | User type      | Authorization |
|--------|-----------------|---------------|
| query | staff only      | required      |


Schema:

```
query learningGroups {
    learningGroups {
        description
        users {
            id
            role
            first_name
        }
    }
}
```
