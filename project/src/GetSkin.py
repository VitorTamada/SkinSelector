import random


class GetSkin:
    def __init__(self, lcu_access):
        self._lcu_access = lcu_access

    def get_available_skins_and_chromas(self):
        result = self._lcu_access.get_available_skins_and_chromas()
        if not result['res']:
            return result

        skins_available = {}
        for skin in result['output'].json():
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
        res = []
        champ_name = ''
        for name, skins in skins_available.items():
            if not champ_name:
                champ_name = skins[0]['name']
            for skin in skins:
                skin_id = skin['id']
                is_chroma_output = ''
                if 'order_num' in skin:
                    skin_id = int(str(skin['parentSkinId'])[-2:])
                    is_chroma_output = "Chroma {}".format(skin['order_num'])
                res.append((champ_name, skin['name'], int(str(skin_id)[-2:]), is_chroma_output))

        if res:
            res = (res[random.randrange(0, len(res))], res)
            res = {'res': True, 'output': res}
        else:
            res = {'res': False, 'output': None}
        return res
