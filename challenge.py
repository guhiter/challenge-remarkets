from argsParser import parseArgs
import reMarketsClient

def main():
    args = parseArgs()

    if(args.bidDif <= 0):
        print('El valor ingresado para [--dif] es inválido')
        return
    if(args.bidPrice <= 0):
        print('El valor ingresado para [--price] es inválido')
    try:
        client = reMarketsClient.myRofexClient(args.apiUser, args.apiPass, args.apiAcc)
        if(client.initialized):
            md = client.getMarketData(args.symbol)
            if(md != None):
                getLastPrice(md)
                bidPrice = getLastBIDPrice(md)
                if(bidPrice != None and bidPrice - args.bidDif > 0):
                    client.placeNewBIDs(args.symbol, bidPrice - args.bidDif, orderType=args.bidOrdType)
                else:
                    client.placeNewBIDs(args.symbol, args.bidPrice, orderType=args.bidOrdType)
    except Exception as ex:
        print('Unhandled exception: {}'.format(ex.msg))

    client.closeClient()
    print('Se ha cerrado la sesión correctamente')

def getLastPrice(marketData):
    ''' Gets LP for a given MarketData and prints result

    :param marketData: Instrument symbol to send in the request
    :type marketData: dict of JSON response
    :return: last price for given MarketData
    :rtype: float

    '''
    successMsg = 'Último precio operado: ${:.2f}'
    errorMsg = 'No posee LP'
    ret = None

    try:
        ret = marketData['LA']['price']
    except:
        print(errorMsg)
    else:
        print(successMsg.format(ret))
        pass
    return ret

def getBids(marketData):
    ''' Gets last BIDs for a given MarketData

    :param marketData: Instrument symbol to send in the request
    :type marketData: dict of JSON response
    :return: last BIDs for given MarketData
    :rtype: dict of JSON response

    '''
    successMsg = 'Se ha obtenido la lista de BIDs'
    errorMsg = 'No hay BIDs activos'
    ret = None

    try:
        ret = marketData['BI']
    except:
        print(errorMsg)
    else:
        # print(successMsg)
        pass
    return ret

def getLastBIDPrice(marketData):
    ''' Gets last BID price for a given MarketData and prints result

    :param marketData: Instrument symbol to send in the request
    :type marketData: dict of JSON response
    :return: last BID price for given MarketData
    :rtype: float

    '''
    successMsg = 'Se ha obtenido el precio de la última BID'
    errorMsg = 'No hay BIDs activos'
    ret = None

    try:
        bids = getBids(marketData)
        ret = bids[0]['price']
        print('Precio de BID: ${:.2f}'.format(ret))
    except:
        print(errorMsg)
    else:
        # print(successMsg)
        pass
    return ret

if __name__ == "__main__":
    main()
