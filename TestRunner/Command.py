
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
    name = 'runscript'
    parser = argparse.ArgumentParser("Run Task")
    parser.add_argument('--task', help="target script to run")

    def execute(self, args):
        """执行过程
        """
        task=args.task
        runner=TaskRunner()
        runner.run(task)


# class RunTest(Command):
#     """批量执行测试用例
#     """
#     name = 'runtest'
#     parser = argparse.ArgumentParser("Run QTA testcases")
#     parser.add_argument("tests", metavar="TEST", nargs='*', help="testcase set to executive, eg: zoo.xxx.HelloTest")
#     parser.add_argument('-w', '--working-dir', default=None, help="working directory to store all result files",
#                         dest="working_dir")
#     # parser.add_argument('--priority', help="run test cases with specific priority, accept multiple options",
#     #                     dest="priorities", action="append",
#     #                     choices=[TestCasePriority.BVT, TestCasePriority.High, TestCasePriority.Normal,
#     #                              TestCasePriority.Low])
#     # parser.add_argument('--status', default=None, help="run test cases with specific status, accept multiple options",
#     #                     dest="status", action="append",
#     #                     choices=[TestCaseStatus.Design, TestCaseStatus.Implement, TestCaseStatus.Ready,
#     #                              TestCaseStatus.Review, TestCaseStatus.Suspend])
#     parser.add_argument("--excluded-name",
#                         help="exclude test cases with specific name prefix , accept multiple options",
#                         action="append", dest="excluded_names", metavar="EXCLUDED_NAME")
#     parser.add_argument("--owner", help="run test cases with specific owner, accept multiple options",
#                         action="append", dest="owners", metavar="OWNER")
#     parser.add_argument("--tag", help="run test cases with specific tag, accept multiple options",
#                         action="append", dest="tags", metavar="TAG")
#     parser.add_argument("--excluded-tag", help="exclude test cases with specific name tag, accept multiple options",
#                         action="append", dest="excluded_tags", metavar="EXCLUDED_TAG")
#
#     # parser.add_argument("--report-type", help="report type", choices=report_types.keys(), default="stream")
#     # parser.add_argument("--report-args", help="additional arguments for specific report", default="")
#     # parser.add_argument("--report-args-help", help="show help information for specific report arguemnts",
#     #                     choices=report_types.keys())
#     #
#     # parser.add_argument("--resmgr-backend-type", help="test resource manager backend type",
#     #                     choices=resmgr_backend_types.keys(), default="local")
#     #
#     # parser.add_argument("--runner-type", help="test runner type", choices=runner_types.keys(), default="basic")
#     # parser.add_argument("--runner-args", help="additional arguments for specific runner", default="")
#     # parser.add_argument("--runner-args-help", help="show help information for specific runner arguemnts",
#     #                     choices=runner_types.keys())


# class RunPlan(Command):
#     """执行测试计划
#     """
#     name = "runplan"
#     parser = argparse.ArgumentParser("Run QTA test plan")
#     parser.add_argument("--report-type", help="report type", choices=report_types.keys(), default="stream")
#     parser.add_argument("--report-args", help="additional arguments for specific report", default="")
#     parser.add_argument("--report-args-help", help="show help information for specific report arguemnts",
#                         choices=report_types.keys())
#
#     parser.add_argument("--runner-type", help="test runner type", choices=runner_types.keys(), default="basic")
#     parser.add_argument("--runner-args", help="additional arguments for specific runner", default="")
#     parser.add_argument("--runner-args-help", help="show help information for specific runner arguemnts",
#                         choices=runner_types.keys())
#
#     parser.add_argument("--resmgr-backend-type", help="test resource manager backend type",
#                         choices=resmgr_backend_types.keys(), default="local")
#
#     parser.add_argument("plan", help="designate a test plan to run")
#
#     def execute(self, args):
#         """执行过程
#         """
#         if args.report_args_help:
#             report_types[args.report_args_help].get_parser().print_help()
#             return
#         if args.runner_args_help:
#             runner_types[args.runner_args_help].get_parser().print_help()
#             return
#
#         report_type = report_types[args.report_type]
#         report = report_type.parse_args(shlex.split(args.report_args))
#
#         resmgr_backend = resmgr_backend_types[args.resmgr_backend_type]()
#
#         runner_type = runner_types[args.runner_type]
#         runner = runner_type.parse_args(shlex.split(args.runner_args), report, resmgr_backend)
#
#         planname = args.plan
#         planmodulename, planclsname = planname.rsplit(".", 1)
#         __import__(planmodulename)
#         planmod = sys.modules[planmodulename]
#         plancls = getattr(planmod, planclsname)
#         runner.run(plancls())

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
        cmp_func = lambda x, y: x > y
        cmds.sort(lambda x, y: cmp_func(x.name, y.name))
        return cmds

    def run(self):
        """执行入口
        """
        cmds = self._load_cmds()
        argparser = ArgumentParser(cmds)
        if len(sys.argv) > 1:
            subcmd, args = argparser.parse_args(sys.argv[1:])
            subcmd.execute(args)
