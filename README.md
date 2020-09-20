爬取网易云音乐并上传至你的ufile

首先请安装以下依赖:

pip3 install pipreqs 

pipreqs . --encoding=utf8 --force

pip3 install -r requirements.txt

pip3 install pycryptodome

cd ufile-sdk-python/

python3 setup.py install

pip3 install ufile

安装完成之后

python3 down_music.py 按提示输入歌曲名称下载歌曲
