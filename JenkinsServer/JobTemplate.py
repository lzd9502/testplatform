CONFIG_XML = '''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>{description}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>true</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.TimerTrigger>
      <spec>{run_time}</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.BatchFile>
      <command>{command}</command>
    </hudson.tasks.BatchFile>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>'''.format

cmd_runner = '\TestRunner\manage.py'


class JobConfig:
    # CONFIG_XML=
    description = r''
    run_time = r''
    command_format = None

    def __init__(self, description=None, run_time=None, task=None):
        self.set_run_time(run_time)
        self.set_description(description)
        self.set_command(task)

    def set_description(self, description):
        self.description = description if description is not None else self.description

    def set_run_time(self, run_time):
        # todo:这里预验证格式合法性
        assert run_time is not None, ('not find \'run_time\' in request data')
        assert type(run_time) is str, ('run_time is not authorized!')
        self.run_time = run_time

    def set_command(self, task):
        assert task is not None, ('not find \'command\' in request data')
        import sys, os
        blank = ' '
        run_type = 'runtask --task'
        run_env = sys.executable
        runner = ''.join((os.path.dirname(os.path.dirname(__file__)), cmd_runner))
        self.command = ''.join((run_env, blank, runner, blank, run_type, blank, str(task)))

    def __call__(self):
        return CONFIG_XML(description=self.description, run_time=self.run_time, command=self.command)


if __name__ == '__main__':
    import sys, os

