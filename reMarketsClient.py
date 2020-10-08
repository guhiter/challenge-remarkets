import pyRofex
import pyRofex.components.exceptions as pExceptions

def initClient(user, password, account=''):
    ''' Initialize the client for Remarkets and handle exceptions.

    :param user: User as shown on Remarkets
    :type user: string
    :param password: Password as shown on Remarkets
    :type password: string
    :param account: Account as shown on Remarkets
    :type account: string
    :return: if initialization was succesful
    :rtype: bool

    '''
    loginMsg = 'Iniciando sesión en Remarkets'
    loginSuccessMsg = 'Ha sido autenticado correctamente'
    loginErrorMsg = 'Fallo en la autenticación, usuario o contraseña inválido'
    ret = False

    print(loginMsg)
    try:
        pyRofex.initialize(user, password, account, pyRofex.Environment.REMARKET)
    except pExceptions.ApiException as ex:
        print(loginErrorMsg)
    else:
        ret = True
        print(loginSuccessMsg)
    return ret

def getMarketData(symbol):
    ''' Checks if the param symbol is valid and returns its market data

    :param symbol: Instrument symbol to send in the request
    :type symbol: string
    :return: Market Data response of the API
    :rtype: dict of JSON response

    '''
    startMsg = 'Consultando símbolo en Remarkets'
    successMsg = 'Se ha obtenido el MarketData del símbolo'
    invalidSymbolMsg = 'El símbolo ingresado es inválido, intente con otro'
    errorMsg = 'Ocurrió un error al consultar la API, inténtelo nuevamente'
    ret = None

    print(startMsg)
    try:
        ret = pyRofex.get_market_data(symbol,
            entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST])
        if(ret['status'] == 'OK'):
            print(successMsg)
            ret = ret['marketData']
        else:
            print(invalidSymbolMsg)
            ret = None
    except pExceptions.ApiException as ex:
        print(errorMsg)
    return ret

def placeNewBIDs(symbol, value, orderType = pyRofex.OrderType.LIMIT, count=1):
    '''Makes a request to the API that sends a new order to the Market

    :param symbol: Instrument symbol to send in the request
    :type symbol: string
    :param symbol: value of the bid to be placed
    :type symbol: float
    :param orderType: Order Type
    :type orderType: OrderType
    :return: if bid placing was succesful
    :rtype: bool

    '''
    startMsg = 'Ingresando orden a ${:.2f}'
    successMsg = 'Se ha ingresado la orden correctamente'
    errorMsg = 'Ocurrió un error al intentar ingresar la orden'
    ret = False

    print(startMsg.format(value))
    try:
        result = pyRofex.send_order(symbol, count, orderType, pyRofex.Side.BUY, price=value, account='REM5149')
        if(result != None and result['status'] == 'OK'):
            print(successMsg)
            ret = True;
    except pExceptions.ApiException as ex:
        print(errorMsg)
    return ret

def closeClient():
    '''

    '''
    startMsg = 'Consultando símbolo en Remarkets'
    successMsg = 'Se ha obtenido el detalle del símbolo'
    errorMsg = 'Símbolo inválido'
    try:
        pass
    except pExceptions.ApiException as ex:
        pass
    else:
        pass
    pass

if __name__ == "__main__":
    pass
