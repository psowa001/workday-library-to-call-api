## **Workday API connector**
Library allow to:
- call Workday API
- get current access token

Library is refreshing tokens when expired in automatic way.

#### Developed with:
- Selenium
- Pyyaml
- Requests

#### Include it in your project:
```
from workday import Workday
```

#### Call Workday API:
```
workday_api = Workday()
workday_api.call_api(query, method)
```

#### Get actual access token:
```
Workday.get_access_token()
```

#### Workday API docs:
https://community.workday.com/sites/default/files/file-hosting/restapi/index.html