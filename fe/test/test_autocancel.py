import pytest
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from be.database import Order, Order_status
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid


class TestCancel:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        engine = create_engine('postgresql://root:123456@localhost:5432/bookstore')
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.seller_id = "test_autocancel_seller_{}".format(str(uuid.uuid1()))
        self.store_id = "test_autocancel_store_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_autocancel_buyer_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)

        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok

        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield


    def test_autocancel(self):
        time.sleep(7)
        cursor = self.session.query(Order).filter_by(id=self.order_id).first()
        assert cursor.status == Order_status.cancelled