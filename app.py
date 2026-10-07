from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect('products.db.sqlite')
    cursor = connection.cursor()

    if request.method == 'POST':
        products_id = request.form.get('product_id')
        units = request.form.get('units')

        if units != None:
            units = int(units)

        print(products_id)
        print(units)

        if products_id != None:
            result = cursor.execute(
                "SELECT * FROM products WHERE product_id=?",
                (products_id,)
            )

            result = tuple(result)

            if len(result) > 0:
                product_name = result[0][1]
                price = result[0][2]
                stocks = result[0][3]

                print(product_name, price, stocks)
                print(type(stocks))
                print(type(units))

                if units != None:
                    if stocks > 0 and units <= stocks:
                        cursor.execute(
                            "UPDATE products SET stock=stock-? WHERE product_id=?",
                            (units, products_id)
                        )

                        connection.commit()

                        stocks = stocks - units

                        print("Sell Complete...")
                    else:
                        print("Not enough stock.")

                else:
                    print("None Value")

                return render_template(
                    'index.html',
                    product_id=products_id,
                    product_name=product_name,
                    price=price,
                    stock=stocks
                )

            else:
                print("Product not found.")

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)