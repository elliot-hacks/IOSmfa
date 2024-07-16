import requests

class MantraSDK:
    def __init__(self, base_url="https://localhost:8003/mfs100/"):
        self.base_url = base_url

    def get_mfs100_info(self):
        return self._get("info")

    def get_mfs100_key_info(self, key):
        data = {
            "Key": key
        }
        return self._post("keyinfo", data)

    def capture_finger(self, quality, timeout):
        data = {
            "Quality": quality,
            "TimeOut": timeout
        }
        return self._post("capture", data)

    def capture_multi_finger(self, quality, timeout, no_of_fingers):
        data = {
            "Quality": quality,
            "TimeOut": timeout,
            "NoOfFinger": no_of_fingers
        }
        return self._post("capturewithdeduplicate", data)

    def verify_finger(self, prob_template, gallery_template):
        data = {
            "ProbTemplate": prob_template,
            "GalleryTemplate": gallery_template,
            "BioType": "FMR"
        }
        return self._post("verify", data)

    def match_finger(self, quality, timeout, gallery_template):
        data = {
            "Quality": quality,
            "TimeOut": timeout,
            "GalleryTemplate": gallery_template,
            "BioType": "FMR"
        }
        return self._post("match", data)

    def get_pid_data(self, biometric_array):
        data = {
            "Biometrics": biometric_array
        }
        return self._post("getpiddata", data)

    def get_rbd_data(self, biometric_array):
        data = {
            "Biometrics": biometric_array
        }
        return self._post("getrbddata", data)

    def _post(self, method, data):
        url = self.base_url + method
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers, verify=False)
        if response.status_code == 200:
            return {"httpStatus": True, "data": response.json()}
        else:
            return {"httpStatus": False, "err": self._get_http_error(response)}

    def _get(self, method):
        url = self.base_url + method
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return {"httpStatus": True, "data": response.json()}
        else:
            return {"httpStatus": False, "err": self._get_http_error(response)}

    def _get_http_error(self, response):
        if response.status_code == 0:
            return 'Service Unavailable'
        elif response.status_code == 404:
            return 'Requested page not found'
        elif response.status_code == 500:
            return 'Internal Server Error'
        else:
            return f"Unhandled Error: {response.status_code}"

