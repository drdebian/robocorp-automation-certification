from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
import pandas as pd


order_csv_url = "https://robotsparebinindustries.com/orders.csv"
order_csv_filename = "orders.csv"
order_website_url = "https://robotsparebinindustries.com/#/robot-order"

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    orders = get_orders()
    print("Found orders:")
    print(orders)

    browser.configure(
        slowmo=1000,
    )

    open_robot_order_website()
    close_annoying_modal()

    # loop through orders
    for i, row in orders.iterrows():
        print(f"Order number {row['Order number']}: Robot with head: {row['Head']}, body: {row['Body']}, legs: {row['Legs']} to address: {row['Address']}")  
        fill_the_form(row)
       

    # create zip archive of the receipts


def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto(order_website_url)

def get_orders():
    """Downloads the order CSV file and returns it as a DataFrame"""
    http = HTTP()
    http.download(order_csv_url, overwrite=True, verify=False)
    df = pd.read_csv(order_csv_filename)
    return df

def close_annoying_modal():
    """Closes the annoying modal that is displayed on the website."""
    page = browser.page()
    page.click("text=OK")   # get rid of the banner by clicking on OK

def fill_the_form(data):
    """Fills the form with the given data and submits it."""
    print(data)
    page = browser.page()
    page.select_option("#head", str(data['Head']))
    page.set_checked(f"#id-body-{str(data['Body'])}", True)
    page.get_by_placeholder("Enter the part number for the legs").fill(str(data['Legs']))
    page.fill("#address", data['Address'])
    # page.click("text=Preview")

    ###<div class="alert alert-danger" role="alert">Have You Tried Turning It On And Off Again?</div>
    ###<div id="receipt" class="alert alert-success" role="alert"><h3>Receipt</h3><div>2024-04-25T11:34:16.451Z</div><p class="badge badge-success">RSB-ROBO-ORDER-PH5MG54JI</p><p>44444</p><div id="parts" class="alert alert-light" role="alert"><div>Head: 1</div><div>Body: 2</div><div>Legs: 4</div></div><p>Thank you for your order! We will ship your robot to you as soon as our warehouse robots gather the parts you ordered! You will receive your robot in no time!</p></div>
    ###<div id="robot-preview-image"><img src="/heads/1.png" alt="Head"><img src="/bodies/2.png" alt="Body"><img src="/legs/4.png" alt="Legs"></div>
    ###<button id="order-another" type="submit" class="btn btn-primary">Order another robot</button>
    # page.click("button:text('Order')")

    # hit submit, until receipt is shown
    while not page.query_selector("#receipt"):
        page.click("button:text('Order')")



    # save receipt as PDF

    # save screenshot of the robot

    # embed screenshot to the PDF

    # load form to order another robot
    page.click("#order-another")
    close_annoying_modal()