import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid


class TestCancel:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_cancel_seller_{}".format(str(uuid.uuid1()))
        self.store_id = "test_cancel_store_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_cancel_buyer_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)

        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok

        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield

    def test_non_exist_buyer(self):
        code = self.buyer.cancel(self.buyer_id + 's', self.password, self.order_id)
        assert code != 200

    def test_wrong_password_buyer(self):
        code = self.buyer.cancel(self.buyer_id, self.password + 's', self.order_id)
        assert code != 200

    def test_ok(self):
        code = self.buyer.cancel(self.buyer_id, self.password, self.order_id)
        assert code == 200