import argparse
from constants import defaultBIDPrice, defaultBIDDif
from pyRofex import OrderType

def parseArgs():
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
    parser.add_argument('--price', default=defaultBIDPrice, type=float,
        help='Valor al cual se debe colocar la orden de compra en ' +
        'el caso que no haya ninguna entrada',
        dest='bidPrice')
    parser.add_argument('--dif', default=defaultBIDDif, type=float,
        help='Diferencia a la cual se debe colocar la orden de compra ' +
        'en caso que exista al menos una entrada',
        dest='bidDif')
    parser.add_argument('--ordType', default=OrderType.LIMIT,
        choices=[OrderType.LIMIT, OrderType.MARKET, OrderType.MARKET_TO_LIMIT],
        help='El tipo de orden que tendrá la BID',
        dest='bidOrdType')
    return parser.parse_args()

if __name__ == "__main__":
    parseArgs()
