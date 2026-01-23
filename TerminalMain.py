"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.1.0
    UpdateTime: 2026-0120-2348
"""

from Utils import JsonReader, Logger
import os, cmd

TEMP = {"MAIN_PATH": os.path.dirname(os.path.realpath(__file__)) + "\\"}

class CgiMain(cmd.Cmd):
    def __init__(self, logger=None, config=None):
        """初始化，接收logger和config参数"""
        super().__init__()  # 调用父类初始化
        self.logger = logger
        self.config = config
        self.prompt = ">>> "  # 自定义提示符
        self.intro = "欢迎使用 ScholarHub 终端! 输入 help 查看命令。"

    def default(self, line):
        """处理未知命令"""
        error_msg = f"未知命令: {line}"
        print(error_msg)
        if self.logger:
            self.logger.warning(error_msg)
        print("输入 'help' 查看可用命令")

    def emptyline(self):
        """空行时的处理"""
        pass  # 默认不执行任何操作

    def postcmd(self, stop, line):
        """命令执行后的处理"""
        print("\n")
        return stop

    def do_help(self, arg):
        """显示帮助信息"""
        if arg:
            # 显示特定命令的帮助
            super().do_help(arg)
        else:
            # 显示通用帮助
            help_text = """
ScholarHub 终端命令列表:
-------------------------
help     - 显示此帮助信息
version  - 显示版本信息
config   - 显示配置信息
exit     - 退出程序
quit     - 退出程序
            """
            print(help_text)

    def do_version(self, arg):
        """显示版本信息"""
        print("ScholarHub Alpha 1.1.0")
        print("Copyright (c) Liszthral")

    def do_config(self, arg):
        """显示配置信息"""
        if self.config:
            print("当前配置:")
            print(f"主路径: {TEMP['MAIN_PATH']}")
            # 显示其他配置信息
        else:
            print("配置未加载")

    def do_exit(self, arg):
        if self.logger:
            self.logger.save_log()
            self.logger.info("用户退出程序")
        return True

    def do_quit(self, arg):
        """退出程序（quit别名）"""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """处理Ctrl+D（Unix）或Ctrl+Z（Windows）"""
        return self.do_exit(arg)

if __name__ == '__main__':
    # 初始化日志和配置
    logger = Logger.Logger(TEMP["MAIN_PATH"] + r"log\log.log")
    logger.info("Started Initialization")
    MainConfig = JsonReader.JsonReader(TEMP["MAIN_PATH"] + r"Configuration\MainConfig.json", logger)

    # 创建CLI实例，传入logger和config
    cli = CgiMain(logger=logger, config=MainConfig)

    try:
        # 启动命令行循环
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n程序被中断")
        logger.warning("程序被键盘中断")

    except Exception as e:
        print(f"发生错误: {e}")
        logger.error(f"程序异常: {e}")
    finally:
        logger.info("程序结束")
