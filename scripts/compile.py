import PyInstaller.__main__ as pyinstaller
import wsgidav.dir_browser as dir_browser
import os

htdocs_src = os.path.join(os.path.dirname(dir_browser.__file__), "htdocs")

pyinstaller.run([
    "../src/fsts_main.py",
    "--onefile",
    "--add-data", "../scripts/windows.bat:fsts-setupFiles",
    "--add-data", "../scripts/linux.sh:fsts-setupFiles",
    "--add-data", "../scripts/mac.sh:fsts-setupFiles",
    "--add-data", "../static/setup_windows.html:static",
    "--add-data", "../static/setup_unix.html:static",
    "--add-data", f"{htdocs_src}:wsgidav/dir_browser/htdocs",
    "--hidden-import", "wsgidav",
    "--hidden-import", "waitress",
    "--hidden-import", "flask",
    "--hidden-import", "werkzeug",
    "--name", "fsts"
])

if (os.path.exists("dist/fsts")):
    os.rename("dist/fsts", "dist/fsts-bin")
else:
    os.rename("dist/fsts.exe", "dist/fsts-bin.exe")