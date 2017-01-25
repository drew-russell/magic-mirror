# Magic Mirror

## Variables that Need to be Populated

### ForecastIO (weather)

- api_key
- lat
- lng

### Sonarr (TV shows)

- sonarr_ip
- sonarr_api

### Google Traffic

- google_api_key
- origin
- destination

The origin and destination should be an address pulled directly from a Google Maps URL. For example, for the White House the origin would be `1600+Pennsylvania+Ave+NW,+Washington,+DC+20500` pulled from `https://www.google.com/maps/place/1600+Pennsylvania+Ave+NW,+Washington,+DC+20500/@38.89768,-77.038671,17z/data=!3m1!4b1!4m5!3m4!1s0x89b7b7bcdec17ee3:0xf920b148b3d45e45!8m2!3d38.8976758!4d-77.0364823`  
