import sys
# Name: Tahseen Ahmad

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QLabel, QComboBox, QCalendarWidget, QDialog, QApplication,
    QGridLayout, QSpinBox
)
from datetime import datetime, timedelta
import csv

class StockTradeProfitCalculator(QDialog):

    def __init__(self):
        super().__init__()

        # Loading stock data from the .csv file given
        self.data = self.make_data()
        if not self.data:
            raise Exception("No stock data loaded!")

        # Defining default date
        first_stock = next(iter(self.data))
        latest_date = sorted(self.data[first_stock].keys())[-1]
        self.sellCalendarDefaultDate = QDate(*latest_date)


        earliest_date = sorted(self.data[first_stock].keys())[0]

        two_weeks_before = tuple(
            map(int, (datetime(*latest_date) - timedelta(days=14)).timetuple()[:3])
        )
        self.buyCalendarDefaultDate = two_weeks_before if two_weeks_before > earliest_date else earliest_date

        # Adding required widgets:
        # Stock selection widget
        self.stockLabel = QLabel("Select Stock:")
        self.stockComboBox = QComboBox()
        self.stockComboBox.addItems(sorted(self.data.keys()))

        # Quantity selection widget
        self.quantityLabel = QLabel("Quantity Purchased:")
        self.quantitySpinBox = QSpinBox()
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(10000)
        self.quantitySpinBox.setValue(1)

        # Purchase date selection widget
        self.purchaseDateLabel = QLabel("Purchase Date:")
        self.purchaseCalendar = QCalendarWidget()
        self.purchaseCalendar.setSelectedDate(QDate(*self.buyCalendarDefaultDate))

        # Sell date selection widget
        self.sellDateLabel = QLabel("Sell Date:")
        self.sellCalendar = QCalendarWidget()
        self.sellCalendar.setSelectedDate(self.sellCalendarDefaultDate)

        # Summary section
        # Creating a label display summary of ser's selections
        self.summaryContainer = QLabel("")

        # Centre aligning
        self.summaryContainer.setAlignment(Qt.AlignmentFlag.AlignCenter)

       # Putting the entire summary section within a border
        self.summaryContainer.setStyleSheet("""
            QLabel {
                border-width: 2px;
                border-style: double;
                border-color: white;
                border-radius: 8px;
                padding: 10px;
            }
        """)
       # When user would select values it would get filled automatically over here
        self.summaryContainer.setText(
            "<b>Summary</b><br>"
            "Stock: <br>"
            "Quantity: <br>"
            "Purchase Date: <br>"
            "Sell Date: "
        )

        # Widget to display total
        self.purchaseTotalLabel = QLabel("Purchase Total: $0.00")
        self.sellTotalLabel = QLabel("Sell Total: $0.00")
        self.profitLabel = QLabel("Profit: $0.00")
        self.lossLabel = QLabel("Loss: $0.00")

        # Creating layout
        layout = QGridLayout()
        layout.addWidget(self.stockLabel, 0, 0)
        layout.addWidget(self.stockComboBox, 0, 1)

        layout.addWidget(self.quantityLabel, 1, 0)
        layout.addWidget(self.quantitySpinBox, 1, 1)

        layout.addWidget(self.purchaseDateLabel, 2, 0)
        layout.addWidget(self.purchaseCalendar, 2, 1)

        layout.addWidget(self.sellDateLabel, 3, 0)
        layout.addWidget(self.sellCalendar, 3, 1)

        # Displaying summary of user selections
        layout.addWidget(self.summaryContainer, 5, 0, 1, 2)

        layout.addWidget(self.purchaseTotalLabel, 6, 0, 1, 2)
        layout.addWidget(self.sellTotalLabel, 7, 0, 1, 2)
        layout.addWidget(self.profitLabel, 8, 0, 1, 2)
        layout.addWidget(self.lossLabel, 9, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("Stock Profit & Loss Tracker")

        # Creating signals
        self.stockComboBox.currentIndexChanged.connect(self.updateUi)
        self.quantitySpinBox.valueChanged.connect(self.updateUi)
        self.purchaseCalendar.selectionChanged.connect(self.updateUi)
        self.sellCalendar.selectionChanged.connect(self.updateUi)

        self.updateUi()

    def updateUi(self):

        # Updating value of total whenever there's a change in widget
        try:
            stock = self.stockComboBox.currentText()
            quantity = self.quantitySpinBox.value()

            # Converting dates into tuples
            selected_purchase_calendar_date = self.purchaseCalendar.selectedDate()
            selected_sell_calendar_date = self.sellCalendar.selectedDate()

            # Converting to strings
            purchase_str = selected_purchase_calendar_date.toString("dd MMM yyyy")
            sell_str = selected_sell_calendar_date.toString("dd MMM yyyy")

            # Updating selection summary whenever stock, quantity or dates changes
            self.summaryContainer.setText(
                f"<b>Summary</b><br>"
                f"Stock: {stock}<br>"
                f"Quantity: {quantity}<br>"
                f"Purchase Date: {purchase_str}<br>"
                f"Sell Date: {sell_str}"
            )
            purchase_date = (selected_purchase_calendar_date.year(), selected_purchase_calendar_date.month(), selected_purchase_calendar_date.day())
            sell_date = ( selected_sell_calendar_date.year(),  selected_sell_calendar_date.month(),  selected_sell_calendar_date.day())

            # Getting prices from dataset
            stock_data = self.data.get(stock, {})
            purchase_price = stock_data.get(purchase_date, 0.0)
            sell_price = stock_data.get(sell_date, 0.0)

            # Calculating total value
            purchase_total = quantity * purchase_price
            sell_total = quantity * sell_price
            profit = sell_total - purchase_total

            # Updating labels
            self.purchaseTotalLabel.setText(f"Purchase Total: ${purchase_total:,.2f}")
            self.sellTotalLabel.setText(f"Sell Total: ${sell_total:,.2f}")
            if profit >= 0:
                self.profitLabel.setText(f"Profit: ${profit:,.2f}")
                self.lossLabel.setText("Loss: $0.00")
            else:
                self.profitLabel.setText("Profit: $0.00")
                self.lossLabel.setText(f"Loss: ${-profit:,.2f}")

        except Exception as e:
            print(f"Error updating UI: {e}")

    def make_data(self):
         # Reading csv file and generating a dictionary structure which returns a dictionary of dictionaries
        data = {}
        try:
            with open('Stock_Market_Dataset.csv', mode='r') as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[1:]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row['Date']
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price_str = row[stock].replace(',', '')
                        try:
                            price = float(price_str)
                        except ValueError:
                            price = 0.0
                        if stock not in data:
                            data[stock] = {}
                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(f"Stocks available: {stock_names}")  # Printing all available stock names

            return data

        except Exception as e:
            print(f"Error reading CSV: {e}")
            return {}

    def string_date_into_tuple(self, date_string):
        '''Converting date in string format (e.g., "2024-02-02") into a tuple (year, month, day)
        which returns a tuple representing the date'''
        try:
            if '-' in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%m/%d/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockTradeProfitCalculator()
    window.show()
    sys.exit(app.exec())
