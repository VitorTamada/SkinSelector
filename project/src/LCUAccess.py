import psutil
import base64
import requests
import certifi

# League Client Update Access


class LCUAccess:
    def __init__(self):
        self._proc_name = "LeagueClientUx.exe"
        self._lcu_api = 'https://127.0.0.1:'
        self._app_port_key = '--app-port'
        self._password_key = '--remoting-auth-token'
        self._header = None
        self._is_lol_running = False

        self.build_header()

    @property
    def header(self):
        return self._header

    @property
    def is_lol_running(self):
        return self._is_league_running()

    def _is_league_running(self):
        running_processes = [p.name() for p in psutil.process_iter()]
        if self._proc_name in running_processes:
            self._is_lol_running = True
            return True
        return False

    def try_request(self, operation, count=0):
        if count > 5:
            return {'res': False, 'output': 'Method _try_request called over 5 times in a row.'}

        if self._lcu_api == 'https://127.0.0.1:' or not self._header:
            return {'res': False, 'output': 'Header empty or command is incomplete:\
                                            \nCommand: {}\
                                            \nHeader: {}'.format(self._lcu_api, self._header)}

        if not isinstance(operation, str):
            return {'res': False, 'output': 'operation argument is not a string.'}

        try:
            command = self._lcu_api + operation
            result = requests.get(command, headers=self._header)
            return {'res': True, 'output': result}

        except requests.exceptions.SSLError:
            print('SSL Error. Adding custom certs to Certifi store...')
            cafile = certifi.where()
            with open('../riotgames.pem', 'rb') as infile:
                customca = infile.read()
            with open(cafile, 'ab') as outfile:
                outfile.write(customca)
            print('That might have worked.')
            return self.try_request(operation, count=count+1)

        except requests.exceptions.ConnectionError as err:
            res = self.build_header()
            if res['res']:
                return self.try_request(operation, count+1)
            return {'res': False, 'output': err}

    def get_available_skins_and_chromas(self):
        return self.try_request('/lol-champ-select/v1/skin-carousel-skins')

    def build_header(self):
        if not self._is_league_running():
            return None

        def _get_process_argument(argument, output):
            return argument.split('{}='.format(output, 1))[1]

        app_port = ''
        password = ''
        try:
            running_processes = {p.name(): p for p in psutil.process_iter()}
            args = running_processes[self._proc_name].cmdline()
            for a in args:
                if self._app_port_key in a:
                    app_port = _get_process_argument(a, self._app_port_key)
                elif self._password_key in a:
                    password = _get_process_argument(a, self._password_key)
        except Exception as e:
            print(u"Unable to get app_port or password: {} / {}".format(app_port, password))
            print(u"Error: {}".format(e))

        if not (app_port and password):
            return {'res': False, 'output': "Couldn't get application port or password from the running process. \
                                            \nApplication port: {} \
                                            \nPassword: {}".format(app_port, password)}

        self._lcu_api = 'https://127.0.0.1:' + app_port
        authorization = str(base64.b64encode(bytes("riot:{}".format(password), 'utf-8')))
        authorization = u"Basic {}".format(authorization.split("'")[1])
        header = {'Authorization': authorization}

        self._header = header

        return {'res': True, 'output': ''}
