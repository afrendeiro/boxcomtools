from boxcomtools.types import Path as _Path, BoxFolder, BoxFile, BoxClient

SECRET_FILE = _Path("~/.imctransfer.auth.json").expanduser().absolute()
APP_REDIRECT_URL = "https://imctransfer.herokuapp.com/"
