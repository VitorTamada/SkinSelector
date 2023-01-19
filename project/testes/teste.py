import psutil
import requests
import certifi
import base64

try:
    # https://hextechdocs.dev/getting-started-with-the-lcu-api/
    # https://www.mingweisamuel.com/lcu-schema/tool/
    # https://riot-api-libraries.readthedocs.io/en/latest/lcu.html
    proc_name = "LeagueClientUx.exe"

    app_port = None
    for p in psutil.process_iter():
        if p.name() == proc_name:
            args = p.cmdline()
            for a in args:
                if '--app-port' in a:
                    app_port = a.split('--app-port=', 1)[1]
                elif '--remoting-auth-token' in a:
                    password = a.split('--remoting-auth-token=', 1)[1]

    lcu_api = 'https://127.0.0.1:'
    if app_port:
        lcu_api += app_port
        print(lcu_api)
    authorization = str(base64.b64encode(bytes("riot:{}".format(password), 'utf-8')))
    authorization = u"Basic {}".format(authorization.split("'")[1])

    print(authorization)

    headers = {'Authorization': authorization}

    response = requests.get(lcu_api + '/lol-champ-select/v1/skin-selector-info', headers=headers)
    print(response.json())

    # every skin the champion has
    # noteworthy fields:
    # - 'unlocked'
    # - 'name'
    # - 'childSkins' - chroma list, with 
    response_skins = requests.get(lcu_api + '/lol-champ-select/v1/skin-carousel-skins', headers=headers)
    print(response_skins)
    print(response_skins.json())
    print(len(response_skins.json()))

    skins_available = {}
    for skin in response_skins.json():
        if not skin['unlocked']:
            continue

        skins_available[skin['name']] = [skin]

        i = 1
        for chroma in skin['childSkins']:
            if not chroma['unlocked']:
                continue

            chroma['order_num'] = i
            skins_available[skin['name']].append(chroma)
            i += 1
    for name, skins in skins_available.items():
        for skin in skins:
            is_chroma = ''
            if len(skins) > 1:
                is_chroma = '(base)'
            if 'order_num' in skin:
                is_chroma = u"(chroma {} - base={})".format(skin['order_num'], int(str(skin['parentSkinId'])[3:]))
            print(u"{} - {} {}".format(name, int(str(skin['id'])[3:]), is_chroma))

except requests.exceptions.SSLError as err:
    print('SSL Error. Adding custom certs to Certifi store...')
    cafile = certifi.where()
    with open('../riotgames.pem', 'rb') as infile:
        customca = infile.read()
    with open(cafile, 'ab') as outfile:
        outfile.write(customca)
    print('That might have worked.')