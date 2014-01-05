from mongoengine import *
connect('stocks')

class Stock(Document):
	symbol = StringField(required=True)
	date = DateTimeField(required=True)
	open_price = DecimalField(required=True)
	high_price = DecimalField(required=True)
	low_price = DecimalField(required=True)
	close_price = DecimalField(required=True)
	volume = DecimalField(required=True)
	adj_close = DecimalField(required=True)
	ema5 = DecimalField()
	ema10 = DecimalField()
	ema12 = DecimalField()
	ema20 = DecimalField()
	ema26 = DecimalField()
	ema52 = DecimalField()
	ema60 = DecimalField()

def get_stocks(symbol_):
	''' all stock data for one symbol '''
	return Stock.objects(symbol=symbol_)

def get_stock(symbol_):
	''' first stock data for one symbol '''
	return Stock.objects(symbol=symbol_).first()

def get_date_stock(symbol_, date_):
	return Stock.objects(symbol=symbol_, date=date_).first()

def new_stock(symbol_, date_, open_, high_, low_, close_, vol_, adj_, ema5_, ema10_, ema12_, ema20_, ema26_, ema52_, ema60_):
	s = Stock(symbol=symbol_, date=date_, open_price=open_, high_price=high_, low_price=low_, close_price=close_, volume=vol_, adj_close=adj_, ema5=ema5_, ema10=ema10_, ema12=ema12_, ema20=ema20_, ema26=ema26_, ema52=ema52_, ema60=ema60_)
	s.save()

def edit_stock(symbol_, date_, key_, val_):
	s = Stock.objects(symbol=symbol_, date=date_).first()
	s.key_ = val_
	s.save()

def del_stock(symbol_, date_):
	s = Stock.projects(symbol=symbol_, date=date_).first()
	s.delete()
