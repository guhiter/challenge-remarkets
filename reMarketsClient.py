import pyRofex
import pyRofex.components.exceptions as pExceptions

class MyRofexClient:
    def __init__(self, user, password, account):
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
        self.user = user
        self.password = password
        self.account = account
        self.initialized = False
        self.webSocketOpen = False
        loginMsg = 'Iniciando sesión en Remarkets'
        loginSuccessMsg = 'Ha sido autenticado correctamente'
        loginErrorMsg = 'Fallo en la autenticación, usuario o contraseña inválido'

        print(loginMsg)
        try:
            pyRofex.initialize(user, password, account, pyRofex.Environment.REMARKET)
        except pExceptions.ApiException as ex:
            print(loginErrorMsg)
        else:
            self.initialized = True
            print(loginSuccessMsg)

    def get_market_data_rest(self, symbol,
        entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST]):
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
            ret = pyRofex.get_market_data(symbol, entries)
            if(ret['status'] == 'OK'):
                print(successMsg)
                ret = ret['marketData']
            else:
                print(invalidSymbolMsg)
                ret = None
        except pExceptions.ApiException as ex:
            print(errorMsg)
        return ret

    def place_new_bids_rest(self, symbol, value, orderType = pyRofex.OrderType.LIMIT, count=1):
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
        failedMsg = 'No se pudo ingresar la orden'
        rejectedMsg = 'La orden ha sido rechazada: {}'
        deniedAccessMsg = 'No tienes acceso a la cuenta {}'
        invalidAccountMsg = 'No existe la cuenta: {}'
        errorMsg = 'Ocurrió un error al intentar ingresar la orden'
        ret = False

        print(startMsg.format(value))
        try:
            result = pyRofex.send_order(symbol, count, orderType, pyRofex.Side.BUY, price=value)
            if(result != None and result['status'] == 'OK'):
                order_status = pyRofex.get_order_status(result['order']['clientId'], result['order']['proprietary'])
                if(order_status != None and order_status['order']['status'] == 'NEW'):
                    print(successMsg)
                    ret = True;
                elif(order_status != None and order_status['order']['status'] == 'REJECTED'):
                    print(rejectedMsg.format(order_status['order']['text']))
                else:
                    print(failedMsg)
            else:
                if(result['message'] == 'Access Denied.'):
                    print(deniedAccessMsg.format(self.account))
                elif(result['message'] == 'Missing required parameter.'):
                    print('NO TIENE CUENTA')
                elif(result['message'] == 'Invalid Account.'):
                    print(invalidAccountMsg.format(self.account))
                else:
                    print(errorMsg + ':' + result['description'])
        except pExceptions.ApiException as ex:
            print(errorMsg)
        return ret



    def _market_data_handler(self,message):
        print("Market Data Message Received: {0}".format(message))
    def _order_report_handler(self,message):
        print("Order Report Message Received: {0}".format(message))
    def _error_handler(self,message):
        print("Error Message Received: {0}".format(message))
    def _exception_handler(self,e):
        print("Exception Occurred: {0}".format(e.message))


    def start_websocket(self,
        market_data_handler=None,
        order_report_handler=None,
        error_handler=None,
        exception_handler=None):
        if(market_data_handler == None):
            market_data_handler = self._market_data_handler
        if(order_report_handler == None):
            order_report_handler = self._order_report_handler
        if(error_handler == None):
            error_handler = self._error_handler
        if(exception_handler == None):
            exception_handler = self._exception_handler
        try:
            if(not self.webSocketOpen):
                pyRofex.init_websocket_connection(
                    market_data_handler=market_data_handler,
                    order_report_handler=order_report_handler,
                    error_handler=error_handler,
                    exception_handler=exception_handler)
                self.webSocketOpen = True
                print("WebSocket iniciado correctamente")
        except pExceptions.ApiException as ex:
            print(ex.msg)

    def subscribe_market_data(self, symbols,
        entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST, pyRofex.MarketDataEntry.OFFERS]):
        try:
            if(self.webSocketOpen):
                pyRofex.market_data_subscription(symbols, entries)
                print('Consultando BID {}'.format(symbols))
            else:
                print('WEBSOCKET cerrado')
        except pExceptions.ApiException as e:
            print("Ocurrió una excepción {}".format(ex.msg))

    def close_websocket(self):
        '''

        '''
        startMsg = 'Consultando símbolo en Remarkets'
        successMsg = 'Se ha obtenido el detalle del símbolo'
        errorMsg = 'Símbolo inválido'
        try:
            if(self.webSocketOpen):
                pyRofex.close_websocket_connection()
                self.webSocketOpen = False
                print("WebSocket cerrado correctamente")
        except pExceptions.ApiException as ex:
            print(ex.msg)


if __name__ == "__main__":
    pass
