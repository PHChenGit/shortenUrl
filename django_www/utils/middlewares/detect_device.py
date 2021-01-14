# pylint: disable=protected-access

import re

from utils.useragent import UserAgent


class DetectDeviceMiddleware:
    def process_request(self, request):    # pylint: disable=no-self-use

        device = 'pc'
        is_garena_mobile = 0
        is_ios = is_android = False

        agent = UserAgent(request.META.get('HTTP_USER_AGENT', ''))

        if agent.is_mobile():
            device = 'mobile'
            if agent._data['os'] == 'iOS':
                is_ios = True
                # do something
            elif agent._data['os'] == 'Android':
                is_android = True
                # do something
            # else:
            # do something

        if re.search('GarenaGas', agent.raw_string) is None:
            is_garena_mobile = 1

        request.session['device'] = device
        request.session['is_ios'] = is_ios
        request.session['is_android'] = is_android
        request.session['is_garena_mobile'] = is_garena_mobile
        request.session['is_checked'] = True

        # return
        # return None
