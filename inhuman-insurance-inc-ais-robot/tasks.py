from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.JSON import JSON
from RPA.Tables import Tables

http = HTTP()
json = JSON()
table = Tables()

TRAFFIC_JSON_FILE_PATH = "output/traffic.json"


@task
def produce_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Produces traffic data work items.
    """
    http.download(
        url="https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",
        target_file=TRAFFIC_JSON_FILE_PATH,
        overwrite=True,
    )
    traffic_data = load_traffic_data_as_table()
    filtered_data = filter_and_sort_traffic_data(traffic_data)
    filtered_data = get_latest_data_by_country(filtered_data)


@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    print("consume")


def load_traffic_data_as_table():
    json_data = json.load_json_from_file(TRAFFIC_JSON_FILE_PATH)
    return table.create_table(json_data["value"])


def filter_and_sort_traffic_data(data):
    rate_key = "NumericValue"
    max_rate = 5.0
    gender_key = "Dim1"
    both_genders = "BTSX"
    year_key = "TimeDim"
    table.filter_table_by_column(data, rate_key, "<", max_rate)
    table.filter_table_by_column(data, gender_key, "==", both_genders)
    table.sort_table_by_column(data, year_key, False)
    return data


def get_latest_data_by_country(data):
    country_key = "SpatialDim"
    data = table.group_table_by_column(data, country_key)
    latest_data_by_country = []
    for group in data:
        first_row = table.pop_table_row(group)
        latest_data_by_country.append(first_row)
    return latest_data_by_country
