### Overview

This module's function is to fetch data from the broker(zerodha) using a token taken from the browser request and its used to create all kind of requests using the broker's api.

### Why

We want a module that can 
 - Export data to a csv
 - Store data in out Database
 - Refresh Data from last loaded

### Zerodha API's
Method: GET
 
```plaintext
https://kite.zerodha.com/oms/instruments/historical/<code>/<time_frame>?user_id=<user_id>&oi=1&from=<yyyy-mm-dd>&to=<yyyy-mm-dd>
```
