from TokenGenerator.TokenGenaretor import *
from StockGetter.stockGetter import *
import json


def sqrPositions():
    import colorama
    from time import sleep
    from datetime import datetime
    now = datetime.now()

    today931 = now.replace(hour=9, minute=31, second=0, microsecond=0)
    today315 = now.replace(hour=15, minute=20, second=0, microsecond=0)
    api = apiSessionCreator()

    try:
        sleep(30)
        ret = api.get_positions()
        for i in ret:
            realised = float(i['rpnl'])
            momentary = float(i['urmtom'])
            netprofit = momentary - realised
            # netprofit = momentary
            if int(i['netqty']) != 0 and netprofit < -5:
                print(f"{i['tsym']} = {i['urmtom']} = {i['netqty']}")
                if (int(i['netqty']) < 0):
                    print(
                        colorama.Fore.RED + colorama.Style.BRIGHT + f"We have to buy {i['tsym']} - {abs(int(i['netqty']))}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
                    place_order(api, "B", i['tsym'], abs(int(i['netqty'])))
                    print(
                        colorama.Fore.RED + colorama.Style.BRIGHT + f"We are squaring off booking loss {netprofit}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
                else:
                    print(
                        colorama.Fore.RED + colorama.Style.BRIGHT + f"We have to Sell {i['tsym']} - {abs(int(i['netqty']))}")
                    place_order(api, "S", i['tsym'], abs(int(i['netqty'])))
                    print(
                        colorama.Fore.RED + colorama.Style.BRIGHT + f"We are squaring off booking loss {netprofit}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
            elif int(i['netqty']) != 0 and netprofit > 3:
                print(f"{i['tsym']} = {i['urmtom']} = {i['netqty']}")
                if (int(i['netqty']) < 0):
                    print(
                        colorama.Fore.GREEN + colorama.Style.BRIGHT + f"We have to buy {i['tsym']} - {abs(int(i['netqty']))}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
                    place_order(api, "B", i['tsym'], abs(int(i['netqty'])))
                    print(
                        colorama.Fore.GREEN + colorama.Style.BRIGHT + f"We are squaring off booking profit {netprofit}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
                else:
                    print(
                        colorama.Fore.GREEN + colorama.Style.BRIGHT + f"We have to Sell {i['tsym']} - {abs(int(i['netqty']))}")
                    place_order(api, "S", i['tsym'], abs(int(i['netqty'])))
                    print(
                        colorama.Fore.GREEN + colorama.Style.BRIGHT + f"We are squaring off booking Profit {netprofit}" + colorama.Fore.RESET + colorama.Style.RESET_ALL)
            else:
                pass
        # if datetime.now() > today315:
        #     print(colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT + f"WE ARE STOPING THE SQR LOOP AS IT IS LATE {datetime.now()}")
        #     break
    except:
        print("Some thing is wrong")



def get_inst_mtm(api):
    import colorama
    ret = api.get_positions()
    mtm = 0
    pnl = 0
    for i in ret:
        mtm += float(i['urmtom'])
        pnl += float(i['rpnl'])
        day_m2m = mtm + pnl
    print(colorama.Fore.MAGENTA +f"Current MTM is {day_m2m}" + colorama.Fore.RESET)

def post():
    api = apiSessionCreator()
    ret = api.get_positions()
    for i in ret:
        # print(i.keys())
        print(f"{i['tsym']} -- {i['netqty']} -- {i['urmtom']} -- {i['rpnl']}")

if __name__ == "__main__":
    post()


