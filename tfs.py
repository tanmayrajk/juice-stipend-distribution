import data_pb2 as data_pb2
import base64

def get_b64_encoded_tfs(dep_airport, arr_airport):
    departure_airport = data_pb2.Airport(name=dep_airport)
    arrival_airport = data_pb2.Airport(name=arr_airport)

    flight_info_1 = data_pb2.FlightInfo(
        date="2025-04-04",
        dep_airport=departure_airport,
        arr_airport=arrival_airport
    )

    flight_info_2 = data_pb2.FlightInfo(
        date="2025-04-11",
        dep_airport=arrival_airport,
        arr_airport=departure_airport
    )

    flight_data = data_pb2.Flight()
    flight_data.flights.append(flight_info_1)
    flight_data.flights.append(flight_info_2)

    serialized_data = flight_data.SerializeToString()
    protobuf_base64 = base64.b64encode(serialized_data).decode()
    return protobuf_base64