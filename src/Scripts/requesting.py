import requests


class Changelog:
    # Fixme: This assumes the old structure where the version key is the only one that matters
    def __init__(self, name, current_ver, release):
        self.name = name
        self.current = current_ver
        self.release = release
        if self.release == "nightly":
            self.url = f"https://pwpupdate.absoluterich.repl.co/{self.name}/"
        else:
            self.url = f"https://absoluterich.repl.co/cornsnake/{self.name}/"

    def get_version(self):
        version = requests.get(self.url + "version.json")
        return version.json()

    def get_changelog(self):
        changelog = requests.get(self.url + "changelog.txt")
        return changelog.text

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
        import requests

        data = {
            "content": message,
        }

        result = requests.post(self.url, json=data)
        if 200 <= result.status_code < 300:
            return result.status_code
        else:
            raise ConnectionError(f"Not sent with {result.status_code}, response: \n{result.json()}")
