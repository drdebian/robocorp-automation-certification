from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import pandas as pd
import os


order_csv_url = "https://robotsparebinindustries.com/orders.csv"
order_csv_filename = "orders.csv"
order_website_url = "https://robotsparebinindustries.com/#/robot-order"
output_directory = "output"
receipts_directory = os.path.join(os.getcwd(), "output", "receipts")
screenshots_directory = os.path.join(os.getcwd(), "output", "screenshots")


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """

    # set up directories
    if not os.path.exists(receipts_directory):
        os.makedirs(receipts_directory)
    else:
        list(
            map(
                os.unlink,
                (
                    os.path.join(receipts_directory, f)
                    for f in os.listdir(receipts_directory)
                ),
            )
        )

    if not os.path.exists(screenshots_directory):
        os.makedirs(screenshots_directory)
    else:
        list(
            map(
                os.unlink,
                (
                    os.path.join(screenshots_directory, f)
                    for f in os.listdir(screenshots_directory)
                ),
            )
        )

    orders = get_orders()
    # print("Found orders:")
    # print(orders)
    print(f"Receipts directory: {receipts_directory}")

    open_robot_order_website()
    close_annoying_modal()

    # loop through orders
    for i, row in orders.iterrows():
        # print(f"Order number {row['Order number']}: Robot with head: {row['Head']}, body: {row['Body']}, legs: {row['Legs']} to address: {row['Address']}")
        fill_the_form(row)

        # store receipt as PDF
        receipt_path = store_receipt_as_pdf(row["Order number"])

        # save screenshot of the robot
        screenshot_path = screenshot_robot(row["Order number"])

        # embed screenshot to the PDF

        # load form to order another robot
        page.click("#order-another")
        close_annoying_modal()

    # create zip archive of the receipts


def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto(order_website_url)
    browser.configure(
        slowmo=500,
    )
    global page
    page = browser.page()


def get_orders():
    """Downloads the order CSV file and returns it as a DataFrame"""
    http = HTTP()
    http.download(order_csv_url, overwrite=True, verify=False)
    df = pd.read_csv(order_csv_filename)
    return df


def close_annoying_modal():
    """Closes the annoying modal that is displayed on the website."""
    # page = browser.page()
    # page.click("text=OK")   # get rid of the banner by clicking on OK
    page.click("//*[@class='btn btn-dark']")


def fill_the_form(data):
    """Fills the form with the given data and submits it."""
    # print(data)
    # page = browser.page()
    page.select_option("#head", str(data["Head"]))
    page.set_checked(f"#id-body-{str(data['Body'])}", True)
    page.get_by_placeholder("Enter the part number for the legs").fill(
        str(data["Legs"])
    )
    page.fill("#address", data["Address"])
    # page.click("text=Preview")

    ###<div class="alert alert-danger" role="alert">Have You Tried Turning It On And Off Again?</div>
    ###<div id="receipt" class="alert alert-success" role="alert"><h3>Receipt</h3><div>2024-04-25T11:34:16.451Z</div><p class="badge badge-success">RSB-ROBO-ORDER-PH5MG54JI</p><p>44444</p><div id="parts" class="alert alert-light" role="alert"><div>Head: 1</div><div>Body: 2</div><div>Legs: 4</div></div><p>Thank you for your order! We will ship your robot to you as soon as our warehouse robots gather the parts you ordered! You will receive your robot in no time!</p></div>
    ###<div id="robot-preview-image"><img src="/heads/1.png" alt="Head"><img src="/bodies/2.png" alt="Body"><img src="/legs/4.png" alt="Legs"></div>
    ###<button id="order-another" type="submit" class="btn btn-primary">Order another robot</button>
    # page.click("button:text('Order')")
    ###<div id="robot-preview-image"><img src="/heads/2.png" alt="Head"><img src="/bodies/3.png" alt="Body"><img src="/legs/3.png" alt="Legs"></div>

    # hit submit, until receipt is shown
    while not page.query_selector("#receipt"):
        page.click("button:text('Order')")


def store_receipt_as_pdf(order_number):
    """Stores the receipt as a PDF file and returns the path to the file."""
    receipt_path = os.path.join(receipts_directory, f"robot-order-{order_number}.pdf")
    receipt_html = page.query_selector("#receipt").inner_html()
    print(f"Receipt HTML: {receipt_html}")
    pdf = PDF()
    pdf.html_to_pdf(receipt_html, receipt_path)
    return receipt_path


def screenshot_robot(order_number):
    """Takes screenshot of ordered robot"""
    screenshot_path = os.path.join(
        screenshots_directory, f"robot-screenshot-{order_number}.png"
    )
    page.query_selector("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path


def embed_screenshot_to_receipt(screenshot, pdf_file):
    pass
