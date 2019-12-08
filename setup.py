import os
from setuptools import setup
from subprocess import Popen, PIPE

def git_tag():
    try:
        cmd = ['git', 'describe', '--tags', '--abbrev=0']
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        proc.stderr.close()
        return proc.stdout.readlines()[0].strip().decode()

    except:
        return "0.1"

data_files = []
dest_theme = "share/themes/Clearine-Fallback/clearine"
dest_conf = "share/clearine"
for directory, _, filenames in os.walk(u'src/data/'):
    for filename in filenames:
        sourcefile = [os.path.join(directory, filename)]
        if filename.endswith(".svg"):
            data_files.append((dest_theme, sourcefile))
        elif filename.endswith(".conf"):
            data_files.append((dest_conf, sourcefile))

print(data_files)

setup(
    name = "Clearine",
    version = git_tag(),
    author = "Nanda Okitavera",
    author_email = "codeharuka.yusa@gmail.com",
    description = ("Beautiful Logout UI for X11 window manager"),
    license = "MIT",
    packages = ["Clearine"],
    package_dir = {"Clearine":  "src"},
    package_data = {"Clearine": ["data/*"]},
    data_files=data_files,
    zip_safe=False,
    url = "https://github.com/okitavera/clearine",
    project_urls = {
        "Source": "https://github.com/okitavera/clearine",
        "Tracker": "https://github.com/okitavera/clearine/issues",
    },
    install_requires = [
        'pygobject',
        'pycairo',
    ],
    entry_points={
        "console_scripts": ["clearine=Clearine.clearine:main"]
    }
)
