def tokenGenerator(sid: str) -> str:
    """
    Please use your respective ID's here
    """
    import pyotp
    import requests
    from urllib.parse import parse_qs, urlparse
    import hashlib


    APIKEY = '8cac21d8da3c4430a357e16423d14d73K'
    secretKey = '2023.80807a86c1ee467ea36a3dbb25119e8fa082af04eb4b9e62K'
    totp_key = '3U3SU2TPECDQKRGFA364DIGSE47477FMK'
    password = '*********'
    userid = 'FT032374'

    passwordEncrpted = hashlib.sha256(password.encode()).hexdigest()
    ses = requests.Session()

    url2 = 'https://authapi.flattrade.in/ftauth'
    payload = {"UserName": userid, "Password": passwordEncrpted, "PAN_DOB": pyotp.TOTP(totp_key).now(), "App": "",
               "ClientID": "", "Key": "", "APIKey": APIKEY, "Sid": sid}
    res2 = ses.post(url2, json=payload)
    reqcodeRes = res2.json()
    parsed = urlparse(reqcodeRes['RedirectURL'])
    reqCode = parse_qs(parsed.query)['code'][0]
    api_secret = APIKEY + reqCode + secretKey
    api_secret = hashlib.sha256(api_secret.encode()).hexdigest()
    payload = {"api_key": APIKEY, "request_code": reqCode, "api_secret": api_secret}
    url3 = 'https://authapi.flattrade.in/trade/apitoken'
    res3 = ses.post(url3, json=payload)
    token = res3.json()['token']
    return token


def tokenWriter():
    global creation_time
    import os
    import datetime

    # Get the path to the file
    file_path = "C:\\Users\\Aditya Narayan Daw\\Desktop\\Int_projects\\stockGetter\\Resource\\token.txt"

    # Get the creation time of the file
    if os.path.exists(file_path):
        creation_time = os.path.getctime(file_path)
        print('Token file path exists')
    else:
        creation_time = '1999-11-04 21:43:16.283209'
        print("Token file path does not exist")
        creation_time = datetime.datetime.fromisoformat(creation_time).timestamp()

    # Convert the creation time to a datetime object
    creation_datetime = datetime.datetime.fromtimestamp(creation_time).date()
    today = datetime.datetime.now().date()

    print(f"Token creation Date - {creation_datetime}")
    print(f"Today's Date - {today}")

    if creation_datetime == today:
        print("This date is today No need to write new token")
        print(f"Current Token is {tokenReader()}")
    else:
        print("Today's token does not exist so we are creating new file with token")
        try:
            os.remove(file_path)
            print("Token File has been removed")
        except FileNotFoundError:
            print("Tried to Remove the token File but path does not exist")
        token = tokenGenerator(getSID())
        with open(file_path, "w") as file:
            file.write(token)
            print("Writing new token is done")


def getSID() -> str:
    import os

    sidFile = "C:\\Users\\Aditya Narayan Daw\\Desktop\\Int_projects\\stockGetter\\Resource\\sid.txt"
    if os.path.exists(sidFile):
        print("SID path exists")
        with open(sidFile, "r") as file:
            sid = file.read()
        print(f"Your sid is {sid}")
        return sid
    else:
        print("No SID is found so failing")
        exit(1)


def tokenReader() -> str:
    file_path = "C:\\Users\\Aditya Narayan Daw\\Desktop\\Int_projects\\stockGetter\\Resource\\token.txt"
    try:
        with open(file_path, "r") as file:
            token = file.read()
        return token
    except IOError:
        print("There is some issue with Reading token from File")
        raise IOError
