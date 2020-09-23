from flask import Flask, request, redirect, abort
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

engine = create_engine('postgresql://postgres:admin@localhost:5432/paybay', echo=True)
currency_list = [c[0] for c in engine.connect().execute(f'select currency from exchange_rates').fetchall()]

def get_order(x):
    return engine.connect().execute(f'select * from orders where order_id={x}').fetchall()

def check_if_id_unique(x):
    if len(get_order(x)) != 0:
        raise AssertionError("id already exists in the database")

def check_currency(x):
    if x not in currency_list:
        raise AssertionError("currency is not valid")

def make_exchange(order, amount, currency):
    if ( order % 2 ) == 0:
        exchange_rate = engine.connect().execute(f'select eur_rate from exchange_rates where currency=\'{currency}\'').fetchone()
    else:
        exchange_rate = engine.connect().execute(f'select usd_rate from exchange_rates where currency=\'{currency}\'').fetchone()
    new_amount = amount * exchange_rate[0]
    return new_amount

@app.route('/pay', methods=['GET','POST'])
def create_order():
    return '''<form action="process">
                  order_id: <input id=order_id type="text" name="order_id"><br>
                  payment_amount: <input id=payment_amount type="text" name="payment_amount"><br>
                  currency: <input id=currency type="text" name="currency"><br>
                  <input id=pay type="submit" value="Pay!"><br>
              </form>'''

@app.route('/process', methods=['GET','POST'])
def insert():
    try:
        order_id = int(request.args.get('order_id'))
        payment_amount = int(request.args.get('payment_amount'))
        currency = request.args.get('currency').upper()
        check_if_id_unique(order_id)
        check_currency(currency)
    except:
        abort(400)

    payment_amount = make_exchange(order_id,payment_amount,currency)

    order = {'order_id': [order_id],'payment_amount': [payment_amount],'currency': [currency]}
    pd.DataFrame(order).to_sql('orders', con=engine, if_exists='append', index=False)
    return redirect('/pay')

@app.route('/process/<int:order_id>', methods=['GET'])
def get(order_id):
    result = get_order(order_id)[0]
    if result:
        return {'order_id': result[0], 'payment_amount': result[1], 'currency': result[2]}
    return {'message: order not found'}, 404

app.run(port=5000)