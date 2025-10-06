# FSTS - FileSystem to Share!
### *Ever wanted to share a file, but it is too big for Discord and E-mail is being a pain?*
Well fear no longer! FSTS acts like a shared drive between you and your friends, so you can all upload and download files to and from it!

Features:
- Cross-Platform (Can most likely run on anyhing python can run on!)
- Basic authentication
- Separate folders for each user to write to, everyone can read!
- A public folder for everyone to read and write to!


## Getting started
### Downloading
Download the binary for your system in releases.

*Alternatively, you can also run the python directly, either by downloading the pre-prepared ZIP (better) or just by downloading the repo*

### Configuration
Configure the program with config.json!

<sup>*People who download the pre-compiled versions will have to create one!*

```json
{
    "HOST": "0.0.0.0",
    "HOSTNAME": "localhost",
    "PORT": 8080,
    "USERS": {
        "user1": "password1",
        "user2": "password2"
    }
}
```
- Host: Put the IP which you want to bind it to. (*Pro tip, use 0.0.0.0 if you don't know what you are doing!*)
- Hostname: Put the domain that *others* will use to connect to it, such as your domain or public IP. If you wish to connect from the same computer that is hosting it, see below.
- Port: Put the port you want to host on
- Users: A table for usernames and passwords for the users authorized to use the program.

#### __FOR SECURITY:__ Please run behind a reverse proxy and use SSL! If you don't, your password will be sent around in plaintext, which is not good.

### Running the pre-compiled program
- Windows

<sup>__WARNING:__ The precompiled .exe is falsely detected by Windows Defender as a virus. Either allow it through, or [run the raw python](#running-the-raw-python).

Just double click the file inside the directory you want to host from!
- Linux

<sup> This will host from whicherever directory you run it in, so be sure it's in the correct spot!

```bash
$ chmod +x ./fsts
> ./fsts
```
- Mac

Since pyinstaller can't cross compile, and I do not have a Mac, I cannot precompile the program for you. You can [run the raw python](#running-the-raw-python).

### Running the raw Python
```bash
python -m pip install -r requirements.txt
python fsts_main.py
```

## Acknowledgements
- [Copyparty](https://github.com/9001/copyparty) for inspiring me to make this!
- [wsgidav](https://github.com/mar10/wsgidav) as the main driver for this project!