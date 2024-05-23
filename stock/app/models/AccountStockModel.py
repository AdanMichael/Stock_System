# coding:utf-8
# 用于用户购买的股票
from . import db
from models import StocksModel , AccountModel

class AccountStockModel(db.Model):
    # 股票与用户多对多关系
    __tablename__ = 'tb_account_stock'
    index = db.Column(db.INTEGER, doc="索引数", nullable=False, autoincrement=True, primary_key=True,)
    stockname = db.Column(db.String(15), doc="股票名称", unique=True, nullable=True)
    stocknum = db.Column(db.String(255), doc="购入数量", nullable=True,default=0)
    buy_time = db.Column(db.String(13), doc="买入时间", nullable=True)
    have_time = db.Column(db.String(255), doc="持有时间", nullable=True)
    buyprice = db.Column(db.DECIMAL(10, 2), doc="买入价格", nullable=True)
    profit=db.Column(db.DECIMAL(10,2), doc="收益", nullable=True)
    account_id= db.Column(db. INTEGER, db.ForeignKey('tb_account.id'))
    code_id = db.Column(db.String(8),db.ForeignKey('tb_stock.code'))

    def to_json(self):
        return {
            'index': self.index,
            'stockname': self.stockname,
            'stocknum': self.stocknum,
            'buy_time': self.buy_time,
            'have_time': self.have_time,
            'buyprice': self.buyprice,
            'pofit':self.profit,
            'account_id':self.account_id,
            'code_id':self.code_id
        }




