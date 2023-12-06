def stocknamereader():
    # importing the module
    import json

    filepath = "C:\\Users\\Aditya Narayan Daw\\Desktop\\Int_projects\\stockGetter\\Resource\\stock.txt"
    # reading the data from the file
    with open(filepath) as f:
        data = f.read()

    # reconstructing the data as a dictionary
    js = json.loads(data)

    print(js)
    return js