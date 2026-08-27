import json

with open("mock_rooms.json", encoding="utf-8") as rooms_json, open("mock_hotels.json", encoding="utf-8") as hotels_json:
    mock_hotels = json.load(hotels_json, )
    mock_rooms = json.load(rooms_json)
    print(f"{mock_hotels=}")
    print(f"{mock_rooms=}")