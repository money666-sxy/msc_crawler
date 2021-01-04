爬取网易云音乐并上传至你的ufile

首先配置ufileup.py的以下字段
```
public_bucket = ''  #公共空间名称(不加后缀)

#private_bucket = '' #私有空间名称(不加后缀)
#localfile = ''  #本地文件名
#put_key = ''  #上传文件在空间中的名称

region = ''

public_key = ''

private_key = ''
```
然后请安装以下依赖:
```

cd msc_crawler/

pip3 install pipreqs 

pipreqs . --encoding=utf8 --force

pip3 install -r requirements.txt

pip3 install pycryptodome

git clone https://github.com/ucloud/ufile-sdk-python.git

cd ufile-sdk-python/

python3 setup.py install

pip3 install ufile
```
安装完成之后

> python3 down_music.py 按提示输入歌曲名称下载歌曲


