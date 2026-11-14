import argparse

from projects.suno_browser_service.apps.login.container import Container

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="独立 Suno 登录窗口；--inspect 只检查现有登录后的表单")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    print(Container().session().open(inspect=args.inspect))
