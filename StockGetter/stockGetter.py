from pandas import DataFrame


def get_time(time_string):
    import time
    data = time.strptime(time_string, '%d-%m-%Y %H:%M:%S')
    return time.mktime(data)


def apiSessionCreator():
    from TokenGenerator.TokenGenaretor import tokenReader
    token = tokenReader()
    password = 'Mita99*daw'
    userid = 'FT032354'

    from NorenRestApiPy.NorenApi import NorenApi

    class FlatTradeApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://piconnect.flattrade.in/PiConnectTP/',
                              websocket='wss://piconnect.flattrade.in/PiConnectWSTp/',
                              eodhost='https://web.flattrade.in/chartApi/getdata/')

    api = FlatTradeApiPy()

    ret = api.set_session(userid=userid, password=password, usertoken=token)

    if ret is not None:
        return api
    else:
        print("Return is None while setting the session fail")
        exit(1)


def stock_printer(*args):
    import pandas as pd
    start_secs = get_time(args[1][0])
    end_secs = get_time(args[1][1])
    token = args[2]

    api = args[0]
    ret = api.get_time_price_series(exchange='NSE', token=token, starttime=start_secs, endtime=end_secs,interval= 5)
    df = pd.DataFrame.from_dict(ret)
    return df

def nifty_printer(*args):
    import pandas as pd
    start_secs = get_time(args[1][0])
    end_secs = get_time(args[1][1])
    token = args[2]

    api = args[0]
    ret = api.get_time_price_series(exchange='NSE', token=token, starttime=start_secs, endtime=end_secs,interval= 5)
    df = pd.DataFrame.from_dict(ret)
    return df



def last_price_greater(df: DataFrame,nifty :DataFrame):
    try:
        if (df.loc[0, 'intc'] > df.loc[1, 'intc']) and (df.loc[1, 'intc'] > df.loc[2, 'intc']) and (
                df.loc[2, 'intc'] > df.loc[3, 'intc']) and (nifty.loc[0, 'intc'] > nifty.loc[2, 'intc']):
            return "Buy"
        elif (df.loc[0, 'intc'] < df.loc[1, 'intc']) and (df.loc[1, 'intc'] < df.loc[2, 'intc']) and (
                df.loc[2, 'intc'] < df.loc[3, 'intc']) and (nifty.loc[0, 'intc'] < nifty.loc[2, 'intc']):
            return "Sell"
        else:
            return "Hold"
    except KeyError as err:
        print(f"There is some issue while validating the Prices - {err}={type(err)}")
        return "None"


def getHoldings(api):
    ret = api.get_holdings()
    return ret


def current_time_creator():
    from datetime import datetime, timedelta
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    before = (datetime.now() - timedelta(minutes=25)).strftime('%d-%m-%Y %H:%M:%S')
    return before, now


def place_order(api, buy_sell,tradingSym,qty):
    import colorama
    ret = api.place_order(buy_or_sell=buy_sell, product_type='I',
                          exchange='NSE', tradingsymbol=tradingSym,
                          quantity=3, discloseqty=0, price_type='MKT', trigger_price=None,
                          retention='DAY', remarks=f'ORDERING TYPE - {buy_sell}')
    print(colorama.Fore.LIGHTBLUE_EX + f"ORDER EXECUTED {ret} FOR {tradingSym}" + colorama.Fore.RESET)


def get_mtm(api):
    from time import sleep
    from datetime import datetime
    import colorama
    now = datetime.now()

    today931 = now.replace(hour=9, minute=31, second=0, microsecond=0)
    today315 = now.replace(hour=15, minute=20, second=0, microsecond=0)
    while True:
        try:
            ret = api.get_positions()
            mtm = 0
            pnl = 0
            day_m2m = 0
            for i in ret:
                mtm += float(i['urmtom'])
                pnl += float(i['rpnl'])
                day_m2m = mtm + pnl
            print(colorama.Fore.LIGHTYELLOW_EX + f"Current MTM profit or loss = {day_m2m}" + colorama.Fore.RESET)
        except Exception as err:
            print(f"There is some issue while calculating MTM {err.args}={type(err)}")
        sleep(60)
        if datetime.now() > today315:
            print(
                colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT + f"WE ARE STOPING THE WHILE LOOP AS IT IS LATE {datetime.now()}")
            break

