from yellowdog_client.object_store.utils import HashUtils


class TestCalculateMd5(object):
    def test(self):
        res = HashUtils.calculate_md5_in_base_64(input_value="my_test_string")

        assert res == 'Cb89xzH5v7bvyZBytv/X8g=='


class TestCalculateMd5Summary(object):
    def test(self):
        res = HashUtils.calculate_md5_summary_in_base_64_url(
            hashes_as_base_64=[
                'DMF1ucDxtqgxw5niaXcmYQ==',             # "a"
                'kutf/uauL+w61xx3dTFXjw==',             # "b"
                'SooI8J03tzeVZJA4QItfMw==',             # "c"
                'gnfgkQ11AZW0SHl2FuCRrQ==',             # "d"
                '4WcXl8UuFfdjOAtF6EHsMg==',             # "e"
            ]
        )

        assert res == 'GMayYo8yl8HdxZASfbS0_w'
