from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for element in positions:
            StockProduct.objects.create(stock=stock, **element)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        positions_instance = instance.positions.all()

        for rec in positions_instance:
            for w in positions:
                if rec.product == w['product']:
                    if 'price' in w:
                        rec.price = w['price']
                    if 'quantity' in w:
                        rec.quantity = w['quantity']
                    if rec.product.id != w['product'].id:
                        StockProduct.objects.create(product=w['product'], price=w['price'], quantity=w['quantity'],
                                                    stock_id=rec.stock_id)
                        rec.save()

        return stock