# This is a sample Python script.


import time
import colorama
from StockGetter.StockNameReader import *
from StockGetter.stockGetter import *
from TokenGenerator.TokenGenaretor import tokenWriter
from threading import Thread
from StockGetter.PortfolioManeger import *


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Importent Functions to Remember

def orderPlacer(api):
    from datetime import datetime

    now = datetime.now()
    qty = 3

    today931 = now.replace(hour=9, minute=31, second=0, microsecond=0)
    today315 = now.replace(hour=15, minute=20, second=0, microsecond=0)

    print(f"Now time {now}")
    print(f"trading start time {today931}")
    print(f"last trading time {today315}")

    while True:
        while today931 < datetime.now() < today315:
            sqrPositions()
            data = stocknamereader()
            for token, tradingSymbol in data.items():
                print("WE ARE CURRENTLY INSIDE FOR LOOP")
                df = stock_printer(api, current_time_creator(), token)[['intc', 'time']]
                niftydf = nifty_printer(api, current_time_creator(), "26000")[['intc', 'time']]
                # df = nifty_printer(api, ("03-11-2023 09:16:00", "03-11-2023 09:31:00"), "26000")[['intc', 'time']]
                call = last_price_greater(df, niftydf)
                print(f"Call We got {call}")
                if call.lower() == "buy":
                    print(
                        colorama.Fore.GREEN + f"WE HAVE GOT BUY SIGNAL - INITIATING BUY {tradingSymbol}" + colorama.Fore.RESET)
                    place_order(api, 'B', tradingSymbol,qty)
                elif call.lower() == "sell":
                    print(
                        colorama.Fore.RED + f"WE HAVE GOT SELL SIGNAL - INITIATING SELL FOR {tradingSymbol}" + colorama.Fore.RESET)
                    place_order(api, 'S', tradingSymbol,qty)
                else:
                    print(f"IT WAS NOT EITHER BUY OR SELL SO NOT EXECUTING ANYTHING {tradingSymbol}")

            time.sleep(360)
            get_inst_mtm(api)
        if datetime.now() > today315:
            print(
                colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT + f"WE ARE STOPING THE WHILE LOOP AS IT IS LATE {datetime.now()}")
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting the Programme")
    tokenWriter()
    api = apiSessionCreator()
    orderPlacer(api)
    print()
