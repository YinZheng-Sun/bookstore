import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid


class TestHistory:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):

        self.seller_id = "test_history_seller_{}".format(str(uuid.uuid1()))
        self.store_id = "test_history_store_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_history_buyer_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)

        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok

        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield

    def test_history(self):
        code, response = self.buyer.history()
        assert code == 200
