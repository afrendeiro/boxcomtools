import typing as tp
import json
import time
import webbrowser

from tqdm import tqdm
import requests
from boxsdk import (
    OAuth2,
    BoxAPIException,
    BoxOAuthException,
)

from boxcomtools import SECRET_FILE, APP_REDIRECT_URL
from boxcomtools.types import Path, BoxFile, BoxFolder, BoxClient


def refresh_token(write: bool = True) -> None:
    """"""
    time.sleep(1)
    print("Refreshing access token...")
    params = json.load(open(SECRET_FILE, "r"))
    params["grant_type"] = "refresh_token"
    resp = requests.post("https://api.box.com/oauth2/token", data=params)
    if not resp.ok:
        print(f"Failure! Could not refresh token.")
        raise ValueError(f"Could not refresh token: {resp.json()}")
    new = resp.json()
    print(f"Success! New token expires in {new['expires_in']} seconds.")

    new_params = json.load(open(SECRET_FILE, "r"))
    new_params["access_token"] = new["access_token"]
    new_params["refresh_token"] = new["refresh_token"]
    if write:
        json.dump(new_params, open(SECRET_FILE, "w"), indent=4)
    if not write:
        return new_params


def get_client(dev_token=None, force_reconnect=False) -> BoxClient:
    """"""

    print("Authenticating with box.com.")

    if dev_token is not None:
        print("Using developer token.")
        secret_params = json.load(open(SECRET_FILE, "r"))
        secret_params = dict(
            client_id=secret_params["client_id"],
            client_secret=secret_params["client_secret"],
            access_token=dev_token,
        )
    else:
        if force_reconnect:
            new_auth()
            secret_params = json.load(open(SECRET_FILE, "r"))
        else:
            try:
                refresh_token()
                secret_params = json.load(open(SECRET_FILE, "r"))
            except ValueError as e:
                # if e.args[-1].endswith("'Refresh token has expired'}"):
                new_auth()
                secret_params = json.load(open(SECRET_FILE, "r"))

    oauth = OAuth2(**secret_params)
    client = BoxClient(oauth)

    # # Test authentication
    # resp = client.session.get("http://ip.jsontest.com/")
    # if not resp.ok:
    #     msg = "Could not authenticate!"
    #     raise BoxAPIException(
    #         msg,
    #         resp.status_code,
    #         msg,
    #         "",
    #         resp.headers,
    #         "http://ip.jsontest.com/",
    #         "GET",
    #         "Authenticating imctransfer app.",
    #     )
    # print("Successful!")

    return client


def new_auth():
    """"""
    secret_params = json.load(open(SECRET_FILE, "r"))
    # New user OAuth
    if "access_token" in secret_params:
        del secret_params["access_token"]

    if "refresh_token" in secret_params:
        del secret_params["refresh_token"]

    oauth = OAuth2(**secret_params)
    auth_url, csrf_token = oauth.get_authorization_url(APP_REDIRECT_URL)
    print("Please copy the code given in the browser webpage and paste the code here.")
    time.sleep(2)
    webbrowser.open(auth_url)
    time.sleep(1)
    (
        secret_params["access_token"],
        secret_params["refresh_token"],
    ) = oauth.authenticate(input("Please enter the code here: "))
    json.dump(secret_params, open(SECRET_FILE, "w"), indent=4)


def get_dir_url_checksums(
    root_dir: BoxFolder,
    json_file: Path = None,
    save_every: int = 10,
    _cur_path: str = None,
) -> tp.Dict:
    """
    Get a dictionary of {'file_path': {'url': 'url_value', 'sha1': 'sha1_value'}}
    recursively for all files within a directory.
    """
    if _cur_path is None:
        _cur_path = root_dir.get().name
    files = dict()
    items = sorted(list(root_dir.get_items()), key=lambda x: x.name)
    for i, item in tqdm(enumerate(items)):
        if i % save_every == 0:
            if json_file is not None:
                existing = json.load(open(json_file, "r"))
                files.update(existing)
                json.dump(files, open(json_file, "w"), indent=4)
        if isinstance(item, BoxFile):
            fp = _cur_path + "/" + item.name
            if fp not in files:
                files[fp] = dict(url=item.get_shared_link_download_url(), sha1=item.sha1)
        elif isinstance(item, BoxFolder):
            files2 = get_dir_url_checksums(
                item,
                json_file,
                save_every,
                _cur_path=_cur_path + "/" + item.name,
            )
            files.update(files2)
    if json_file is not None:
        json.dump(files, open(json_file, "w"), indent=4)
    return files
