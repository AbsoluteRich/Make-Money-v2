import requests

# Todo: Finish changelog


class Changelog:
    # Fixme: This assumes the old structure where the version key is the only one that matters
    def __init__(self, name, current_ver, release, url):
        self.name = name
        self.current = current_ver
        self.release = release
        self.url = url  # Host prefix

    # Get functions: Raw data
    def get_version(self):
        version = requests.get(self.url + "version.json")
        return version.json()

    def get_changelog(self, release):
        changelog = requests.get(self.url + f"{release}.txt")
        return changelog.text

    # Find functions: Processed versions for code use
    def find_

    def up_to_date(self):

        def convert_version(number):
            return tuple(number.split("."))

        if self.release != "nightly":
            local = convert_version(self.current)

            remote = self.get_version()
            remote = remote[self.release]
            remote = convert_version(remote)

            if local[0] < remote[0]:
                return False, "major"
            elif local[1] < remote[1]:
                return False, "minor"
            elif local[2] < remote[2]:
                return False, "patch"
            else:
                return True

        else:
            remote = self.get_version()
            remote = remote[self.release]

            if not remote:
                return False
            else:
                return True


class Webhook:
    def __init__(self, url):
        self.url = url

    def send(self, message):
        data = {
            "content": message,
        }

        result = requests.post(self.url, json=data)

        # Returns a tuple with the following information:
        # - If the request succeeded or not
        # - The HTTP status code
        # - The request's JSON
        if 200 <= result.status_code < 300:
            return True, result.status_code, None
        else:
            return False, result.status_code, result.json()
