CONFIG_XML='''
<?xml version='1.1' encoding='UTF-8'?>
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
</project>
'''.format

class JobConfig:
    # CONFIG_XML=
    description=r''
    run_time=r''
    command=r''
    def set_description(self,description):
        assert type(description) is str,('run_time is not authorized!')
        self.description=description
    def set_run_time(self,run_time):
        #todo:这里预验证格式合法性
        assert type(run_time) is str,('run_time is not authorized!')
        self.run_time=run_time
    def set_command(self,command):
        assert type(command) is str,('run_time is not authorized!')
        self.command=command
    def __call__(self, *args, **kwargs):
        return CONFIG_XML(description=self.description,run_time=self.run_time,command=self.command)

