import argparse
from constants import defaultBIDPrice, defaultBIDDif, defaultOrdType
from pyRofex import OrderType

def my_parse_args():
    parser = argparse.ArgumentParser(description=
        'Consultar sobre Remarkets el BID de un símbolo e ingresar una orden ' +
        'de compra a ${:.2f} menos de la última entrada o '.format(defaultBIDDif) +
        'a ${:.2f} en caso que no haya ninguna'.format(defaultBIDPrice),
        add_help=True)
    parser.add_argument('-s', '--symbol', required=True,
        help='Símbolo a consultar en el mercado (Remarkets), ' +
        'y posteriormente colocar una orden de compra',
        dest='symbol')
    parser.add_argument('-u', '--user', required=True,
        help='Usuario de la cuenta de Remarkets para utilizar la API',
        dest='apiUser')
    parser.add_argument('-p', '--password', required=True,
        help='Contraseña de la cuenta de Remarkets para utilizar la API',
        dest='apiPass')
    parser.add_argument('-a', '--account', required=True,
        help='Valor de la cuenta de Remarkets para utilizar la API',
        dest='apiAcc')
    parser.add_argument('--price', default=defaultBIDPrice, type=float,
        help='Valor al cual se debe colocar la orden de compra en ' +
        'el caso que no haya ninguna entrada',
        dest='bidPrice')
    parser.add_argument('--dif', default=defaultBIDDif, type=float,
        help='Diferencia a la cual se debe colocar la orden de compra ' +
        'en caso que exista al menos una entrada',
        dest='bidDif')
    parser.add_argument('--ordType', default=defaultOrdType,
        choices=['limit', 'market', 'market_to_limit'],
        help='El tipo de orden que tendrá la BID',
        dest='bidOrdType')

    args = parser.parse_args()
    if(args.bidOrdType == 'market_to_limit'):
        args.bidOrdType = OrderType.MARKET_TO_LIMIT
    elif(args.bidOrdType == 'market'):
        args.bidOrdType = OrderType.MARKET
    else:
        args.bidOrdType = OrderType.LIMIT
    return args

if __name__ == "__main__":
    parseArgs()
