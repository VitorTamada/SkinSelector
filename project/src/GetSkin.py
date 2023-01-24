import random


# Skins that are considered to have a chroma despite not actually having any.
skins_chroma_exception = [
    'K/DA ALL OUT SERAPHINE INDIE'
]


class GetSkin:
    def __init__(self, lcu_access):
        self._lcu_access = lcu_access

    @staticmethod
    def _get_unlocked_skins(request_result):
        unlocked_skins = {}
        for skin in request_result['output'].json():
            if not skin['unlocked']:
                continue

            unlocked_skins[skin['name']] = [skin]

            i = 1
            for chroma in skin['childSkins']:
                if not chroma['unlocked']:
                    continue

                if chroma['name'] == skin['name'] and not chroma['name'].upper() in skins_chroma_exception:
                    unlocked_skins[skin['name']].append(chroma)
                    chroma['order_num'] = i
                    i += 1
                else:
                    unlocked_skins[chroma['name']] = [chroma]

        return unlocked_skins

    @staticmethod
    def _filter_unlocked_skins(unlocked_skins):
        filtered_unlocked_skins = []
        champ_name = ''
        for name, skins in unlocked_skins.items():
            if not champ_name:
                champ_name = skins[0]['name']

            for skin in skins:
                skin_id = skin['id']
                is_chroma_output = ''
                if 'order_num' in skin:
                    skin_id = int(str(skin['parentSkinId'])[-2:])
                    is_chroma_output = "Chroma {}".format(skin['order_num'])
                filtered_unlocked_skins.append((champ_name,
                                                skin['name'],
                                                int(str(skin_id)[-2:]),
                                                (is_chroma_output, skin['chromaPreviewPath'])))

        return filtered_unlocked_skins

    def get_available_skins_and_chromas(self):
        request_result = self._lcu_access.get_available_skins_and_chromas()
        if not request_result['res']:
            return request_result

        unlocked_skins = self._get_unlocked_skins(request_result)
        filtered_unlocked_skins = self._filter_unlocked_skins(unlocked_skins)

        if filtered_unlocked_skins:
            filtered_unlocked_skins = (filtered_unlocked_skins[random.randrange(0, len(filtered_unlocked_skins))], filtered_unlocked_skins)
            filtered_unlocked_skins = {'res': True, 'output': filtered_unlocked_skins}
        else:
            filtered_unlocked_skins = {'res': False, 'output': None}
        return filtered_unlocked_skins
