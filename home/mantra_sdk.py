import requests
import json

class MantraSDK:
    def __init__(self, uri="https://localhost:8003/mfs100/"):
        self.uri = uri

    def _post(self, method, data):
        url = self.uri + method
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return {'httpStatus': True, 'data': response.json()}
        except requests.exceptions.HTTPError as errh:
            return {'httpStatus': False, 'err': self._get_http_error(response.status_code)}
        except requests.exceptions.RequestException as err:
            return {'httpStatus': False, 'err': str(err)}

    def _get(self, method):
        url = self.uri + method
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {'httpStatus': True, 'data': response.json()}
        except requests.exceptions.HTTPError as errh:
            return {'httpStatus': False, 'err': self._get_http_error(response.status_code)}
        except requests.exceptions.RequestException as err:
            return {'httpStatus': False, 'err': str(err)}

    def _get_http_error(self, status_code):
        if status_code == 0:
            return 'Service Unavailable'
        elif status_code == 404:
            return 'Requested page not found'
        elif status_code == 500:
            return 'Internal Server Error'
        else:
            return 'Unhandled Error'

    def get_mfs100_info(self):
        return self._get("info")

    def get_mfs100_key_info(self, key):
        data = {"Key": key}
        return self._post("keyinfo", data)

    def capture_finger(self, quality, timeout):
        data = {"Quality": quality, "TimeOut": timeout}
        return self._post("capture", data)

    def capture_multi_finger(self, quality, timeout, no_of_finger):
        data = {"Quality": quality, "TimeOut": timeout, "NoOfFinger": no_of_finger}
        return self._post("capturewithdeduplicate", data)

    def verify_finger(self, prob_fmr, gallery_fmr):
        data = {
            "ProbTemplate": prob_fmr,
            "GalleryTemplate": gallery_fmr,
            "BioType": "FMR"
        }
        return self._post("verify", data)

    def match_finger(self, quality, timeout, gallery_fmr):
        data = {
            "Quality": quality,
            "TimeOut": timeout,
            "GalleryTemplate": gallery_fmr,
            "BioType": "FMR"
        }
        return self._post("match", data)

    def get_pid_data(self, biometric_array):
        data = {"Biometrics": biometric_array}
        return self._post("getpiddata", data)

    def get_rbd_data(self, biometric_array):
        data = {"Biometrics": biometric_array}
        return self._post("getrbddata", data)

# Classes to represent Biometric data
class Biometric:
    def __init__(self, bio_type, biometric_data, pos, nfiq, na):
        self.BioType = bio_type
        self.BiometricData = biometric_data
        self.Pos = pos
        self.Nfiq = nfiq
        self.Na = na

class MFS100Request:
    def __init__(self, biometric_array):
        self.Biometrics = biometric_array
