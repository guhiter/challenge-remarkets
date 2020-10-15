from argsParser import my_parse_args
import reMarketsClient

def main():
    args = my_parse_args()

    if(args.bidDif <= 0):
        print('El valor ingresado para [--dif] es inválido')
        return
    if(args.bidPrice <= 0):
        print('El valor ingresado para [--price] es inválido')
        return

    challenge = Challenge(args.apiUser, args.apiPass, args.apiAcc)
    challenge.subscribe_market_data_and_place_bid(args.symbol, args.bidDif, args.bidPrice, args.bidOrdType)

class Challenge:
    def __init__(self, apiUser, apiPass, apiAcc):
        try:
            self.client = reMarketsClient.MyRofexClient(apiUser, apiPass, apiAcc)
            if(self.client.initialized):
                self.client.start_websocket(
                    market_data_handler=self.market_data_handler,
                    error_handler=self.error_handler)
        except Exception as ex:
            print('Excepcion no capturada: {}'.format(ex))

    def subscribe_market_data_and_place_bid(self, symbol, bidDif, bidDefPrice, bidOrdType):
        self.symbol = symbol
        self.bidDif = bidDif
        self.bidDefPrice = bidDefPrice
        self.bidOrdType = bidOrdType

        self.client.subscribe_market_data([symbol])

    def market_data_handler(self, message):
        # startMsg = 'Consultando símbolo en Remarkets'
        successMsg = 'Se ha obtenido el MarketData del símbolo'
        invalidSymbolMsg = 'El símbolo ingresado es inválido, intente con otro'
        errorMsg = 'Ocurrió un error al consultar la API, inténtelo nuevamente'
        ret = None

        print(successMsg)
        md = message['marketData']
        self.get_last_price(md)
        bidPrice = self.get_last_bid_price(md)
        if(bidPrice != None and bidPrice - self.bidDif > 0):
            self.client.place_new_bids_rest(self.symbol, bidPrice - self.bidDif, orderType=self.bidOrdType)
        else:
            self.client.place_new_bids_rest(self.symbol, self.bidDefPrice, orderType=self.bidOrdType)

        self.client.close_websocket()



    # def order_report_handler(self,message):
    #     print("Order Report Message Received: {0}".format(message))
    def error_handler(self,message):
        print("No existe el símbolo solicitado")
        self.client.close_websocket()
    def exception_handler(self,e):
        print("Exception Occurred: {0}".format(e.message))
        self.client.close_websocket()

    def get_last_price(self, marketData):
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

    def get_bids(self, marketData):
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

    def get_last_bid_price(self, marketData):
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
