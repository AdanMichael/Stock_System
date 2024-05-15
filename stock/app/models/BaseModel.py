# coding:utf-8
# 指数、行业、概念（包括基金，债券，美股，外汇，期货，黄金等的代码）模型

from . import db


class BaseModel(db.Model):
    """ 指数、行业、概念 """
    __tablename__ = 'tb_base'
    id = db.Column(db.Integer, doc="id", primary_key=True)
    code = db.Column(db.String(255), doc="code", nullable=True)
    name = db.Column(db.String(255), doc="名称", nullable=True)
    type1 = db.Column(db.Integer, doc="一级分类", nullable=True)
    type2 = db.Column(db.Integer, doc="二级分类", nullable=True)
    level = db.Column(db.Integer, doc="层级", nullable=True)
    pcode = db.Column(db.String(255), doc="父节点代码", nullable=True)
    pname = db.Column(db.String(255), doc="父节点名称", nullable=True)
    isleaf = db.Column(db.Integer, doc="是否叶子节点", nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type1': self.type1,
            'type2': self.type2,
            'level': self.level,
            'pcode': self.pcode,
            'pname': self.pname,
            'isleaf': self.isleaf
        }