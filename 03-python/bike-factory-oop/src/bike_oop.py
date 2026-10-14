"""Bike factory example rewritten using Object-Oriented Programming."""


class Bike:
    def __init__(self, description, cost, sale_price, condition):
        # Encapsulation: store the bike's data in private attributes.
        self.__description = description
        self.__cost = cost
        self.__sale_price = sale_price
        self.__condition = condition
        self.__sold = False

    @property
    def description(self):
        return self.__description

    @property
    def cost(self):
        return self.__cost

    @property
    def sale_price(self):
        return self.__sale_price

    @property
    def condition(self):
        return self.__condition

    @property
    def sold(self):
        return self.__sold

    def update_sale_price(self, sale_price):
        if self.__sold:
            print('Action not allowed, Bike has already been sold')
        else:
            self.__sale_price = sale_price

    def sell(self):
        self.__sold = True

    def display_details(self):
        print(f'Description: {self.__description}')
        print(f'Cost: {self.__cost}')
        print(f'Sale price: {self.__sale_price}')
        print(f'Condition: {self.__condition}')
        print(f'Sold: {self.__sold}')


# Create a Bike object with the same data as the original program.
bike1 = Bike('Univega Alpina, orange', cost=100, sale_price=500, condition=0.5)

# Update the price before selling the bike.
bike1.update_sale_price(350)

# Sell the bike.
bike1.sell()

# Display the final state of the bike.
bike1.display_details()

# Updating the price after selling is not allowed.
bike1.update_sale_price(300)