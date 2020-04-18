## API Docs

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

### Interface to get social user status

| URI                               | Method | Authorization |
|-----------------------------------|--------|---------------|
|`api/v1/status/<social user id>/`  | `GET`  | not required  |

Success Response:
* Code: 200
* Content: `{"status": <status_id>}`, where `status_id` is the current status of the social user in the application.
* Possible values of the `status_id`:
    - `new` - the social user have not applied for join
    - `pending` - the social user already had applied for join but application administrator have not linked him/her with a particular application user
    - `user` -  the social user is the legitimate user of the application
