from src.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, index=True, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )
    date_deleted = db.Column(db.DateTime, default=None)

    def save(self):
        """
        Save model instance.
        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """
        Delete model instance.
        :return:
        """
        db.session.delete(self)
        return db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        """
        Find data by id
        :param id:
        :return:
        """
        return cls.query.get_or_404(id)

    @classmethod
    def find_all(cls, order=None):
        """
        Find all non-deleted data
        :return:
        """
        if order is None:
            order = cls.date_created.desc()
        return cls.query.filter(cls.date_deleted.is_(None)).order_by(order).all()

    def search(self, condition):
        """
        Search data by condition
        :return:
        """
        pass
