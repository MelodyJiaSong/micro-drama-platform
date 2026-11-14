def pytest_configure(config):
    config.addinivalue_line("markers", "single_review: 用正式名册（Claude 单审，chuanyue_yiri follow-up 065）跑，不换成双审副本")
