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


class JobConfig:
    # CONFIG_XML=
    description = r''
    run_time = r''
    command_format = r'E:\Py2VirEnvs\testplatform\Scripts\python.exe C:/Users/Administrator/Documents/GitHub/testplatform/TestRunner/manage.py RunTask --task {Task_id}'.format

    def __init__(self, description=None,run_time=None,command=None):
        self.set_run_time(run_time)
        self.set_description(description)
        self.set_command(command)

    def set_description(self, description):
        assert type(description) is str, ('run_time is not authorized!')
        self.description = description if description is not None else self.description

    def set_run_time(self, run_time):
        # todo:这里预验证格式合法性
        assert run_time is not None, ('not find \'run_time\' in request data')
        assert type(run_time) is str, ('run_time is not authorized!')
        self.run_time = run_time

    def set_command(self, command):
        assert command is not None, ('not find \'command\' in request data')
        assert type(command) is str, ('run_time is not authorized!')
        self.command = self.command_format(command)

    def __call__(self):
        return CONFIG_XML(description=self.description, run_time=self.run_time, command=self.command)