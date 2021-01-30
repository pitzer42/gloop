curl -X POST -d '_id=bar' -d '_description=dummy' localhost:8080/rooms
curl -X GET localhost:8080/rooms
curl -X GET localhost:8080/rooms/bar