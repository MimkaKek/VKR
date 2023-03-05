#!/bin/bash

curl -d '{"user":{"name": "User1", "mail":"example1@example.net","pass":"pas1"}}' \
     -H "Content-Type: application/json" \
     -X GET http://localhost:8000/users \