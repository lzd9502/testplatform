
import argparse
import inspect
import os
import sys
sys.path.append(os.path.dirname(__file__))
from TestRunner.Runner import TaskRunner

class ArgumentParser(object):
    """参数解析
    """
    USAGE = """Usage: %(ProgramName)s subcommand [options] [args]

Options:
  -h, --help            show this help message and exit

Type '%(ProgramName)s help <subcommand>' for help on a specific subcommand.

Available subcommands:

%(SubcmdList)s

"""

    def __init__(self, subcmd_classes):
        """构造函数
        """
        self.subcmd_classes = subcmd_classes
        self.prog = os.path.basename(sys.argv[0])

    def print_help(self):
        """打印帮助文档
        """
        # logger.info(self.USAGE % {"ProgramName": self.prog,
        #                           "SubcmdList": "\n".join(['\t%s' % it.name for it in self.subcmd_classes])})

    def parse_args(self, args):
        """解析参数
        """
        if len(args) < 1:
            self.print_help()
            sys.exit(1)

        subcmd = args[0]
        for it in self.subcmd_classes:
            if it.name == subcmd:
                subcmd_class = it
                parser = it.parser
                break
        else:
            # logger.error("invalid subcommand \"%s\"\n" % subcmd)
            sys.exit(1)

        ns = parser.parse_args(args[1:])
        subcmd = subcmd_class()
        subcmd.main_parser = self
        return subcmd, ns

    #     def add_subcommand(self, subcmd, parser ):
    #         """增加一个子命令
    #         """
    #         parser.prog = "%s help" % self.prog
    #         self._subcmd_parser_dict[subcmd] = parser

    def get_subcommand(self, name):
        """获取子命令
        """
        for it in self.subcmd_classes:
            if it.name == name:
                return it()


class Command(object):
    """一个命令
    """
    name = None
    parser = None

    def execute(self, args):
        """执行过程
        """
        raise NotImplementedError()


class Help(Command):
    """帮助命令
    """
    name = 'help'
    parser = argparse.ArgumentParser("Display subcommand usage")
    parser.add_argument('subcommand', nargs='?', help="target subcommand to display")

    def execute(self, args):
        """执行过程
        """
        if args.subcommand == None:
            self.main_parser.print_help()
        else:
            subcmd = self.main_parser.get_subcommand(args.subcommand)
            subcmd.parser.print_help()


class RunTask(Command):
    """执行一个脚本
    """
    name = 'runtask'
    parser = argparse.ArgumentParser("Run Task")
    parser.add_argument('--task', help="target script to run")

    def execute(self, args):
        """执行过程
        """
        task=args.task
        runner=TaskRunner()
        runner.run(task)
class RunCase(Command):
    name='runcase'
    def execute(self, args):
        pass


# class ManagementToolsConsole(object):
#     """管理工具交互模式
#     """
#     prompt = "QTA> "
#
#     def __init__(self, argparser):
#         self._argparser = argparser
#
#     def cmdloop(self):
#         logger.info("""QTAF %(qtaf_version)s (test project: %(proj_root)s [%(proj_mode)s mode])\n""" % {
#             'qtaf_version': version,
#             'proj_root': settings.PROJECT_ROOT,
#             'proj_mode': settings.PROJECT_MODE,
#         })
#         if six.PY3:
#             raw_input_func = input
#         else:
#             raw_input_func = raw_input
#         while 1:
#             line = raw_input_func(self.prompt)
#             args = shlex.split(line, posix="win" not in sys.platform)
#             if not args:
#                 continue
#             subcmd = args[0]
#             if not self._argparser.get_subcommand(subcmd):
#                 sys.stderr.write("invalid command: \"%s\"\n" % subcmd)
#                 continue
#             try:
#                 subcmd, ns = self._argparser.parse_args(args)
#                 subcmd.execute(ns)
#             except SystemExit:
#                 logger.info("command exit")
#             except:
#                 traceback.print_exc()

class ManagementTools(object):
    """管理工具类入口
    """
    excluded_command_types = []

    def __init__(self):
        pass

    def _load_cmds(self):
        """加载全部的命令
        """
        cmds = []
        cmds += self._load_cmd_from_module(sys.modules[__name__])
        return cmds

    def _load_cmd_from_module(self, mod):
        """加载一个模块里面的全部命令
        """
        cmds = []
        for objname in dir(mod):
            obj = getattr(mod, objname)
            if not inspect.isclass(obj):
                continue
            if obj == Command:
                continue
            if obj in self.excluded_command_types:
                continue
            if issubclass(obj, Command):
                cmds.append(obj)
        # cmp_func = lambda x, y: x > y
        # cmds.sort(lambda x, y: cmp_func(x.name, y.name))
        return cmds

    def run(self):
        """执行入口
        """
        cmds = self._load_cmds()
        argparser = ArgumentParser(cmds)
        if len(sys.argv) > 1:
            subcmd, args = argparser.parse_args(sys.argv[1:])
            subcmd.execute(args)
