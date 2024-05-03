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
    table.write_table_to_csv(traffic_data, "output/test.csv")


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
