# Challenge Remarkets

Consultar sobre Remarkets el BID de un símbolo e ingresar una orden de compra a $0.01 menos de la última entrada o a $75.25 en caso que no haya ninguna.

## Requisitos
- pipenv


## Uso

```shell
challenge.py [-h] -s SYMBOL -u APIUSER -p APIPASS -a APIACC [--price BIDPRICE] [--dif BIDDIF] [--ordType {limit,market,market_to_limit}]

$challenge.py -s 'DOOct20' -u '<user>' -p '<pass>' -a '<account_name>'
```
