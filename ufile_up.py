
from ufile import filemanager
from ufile import bucketmanager
from ufile import config

public_bucket = ''  # 公共空间名称(不加后缀)
# private_bucket = '' # 私有空间名称(不加后缀)
localfile = ''  # 本地文件名
put_key = ''  # 上传文件在空间中的名称
region = ''
public_key = ''
private_key = ''


# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
config.set_default(uploadsuffix='.{0}.{1}.ufileos.com'.format(public_bucket,region))
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='.{}.ucloud.com.cn'.format(public_bucket))
# 设置请求连接超时时间，单位为秒
config.set_default(connection_timeout=60)
# 设置私有bucket下载链接有效期,单位为秒
config.set_default(expires=60)
# 设置上传文件是否校验md5
config.set_default(md5=True)



def put_file(localfile: str, put_key: str):
    # 增 传入本地文件路径、文件云上空间名称，将文件上传至ufile
    putufile_handler = filemanager.FileManager(public_key, private_key)
    # 普通上传文件至公共空间
    ret, resp = putufile_handler.putfile(
        public_bucket, put_key, localfile, header=None)
    assert resp.status_code == 200
    download_addr = 'http://{0}.{1}.ufileos.com/'.format(public_bucket,region)+put_key
    print('下载链接:',download_addr)
    return download_addr


if __name__ == "__main__":
    a = put_file(localfile, put_key)
    print(a)

