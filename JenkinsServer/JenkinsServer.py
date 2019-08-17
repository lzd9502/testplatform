import jenkins


class Jenkins:
    url = 'http://127.0.0.1:8080'
    username = 'lzd9502'
    password = '19950223'
    def CreateJenkinsServer(self):
        server = jenkins.Jenkins(self.url, username=self.username, password=self.password)
        return server

    def set_url(self, url):
        self.url = url

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password
