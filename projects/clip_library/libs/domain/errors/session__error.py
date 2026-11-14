class NotLoggedInError(Exception):
    def __init__(self) -> None:
        super().__init__("没有读到 YouTube 登录状态：请在弹出的 Chrome 里登录成功后再关闭窗口")
