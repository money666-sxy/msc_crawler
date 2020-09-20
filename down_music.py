import requests
import random
import math
from Crypto.Cipher import AES
import base64
import codecs
import os
import ufile_up
"""
获取歌曲地址：https://music.163.com/weapi/song/enhance/player/url?csrf_token=429d8812f4449bb9acb60e7647113999
"""


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',

        }

    def get_songs(self, name):
        d = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}' % name
        wyy = AesDecode(d)    # 要搜索的歌曲名在这里
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        # print(response['result']['songs'][0]['name'])
        # print(response['result']['songs'][0]['al']['picUrl'])
        # print(response)
        return response

    def get_songs_list(self, name):
        response = self.get_songs(name)['result']
        pic_url = response['songs'][0]['al']['picUrl']
        mus_url = self.get_mp3(response['songs'][0]['id'])
        song_list = []
        for num, song in enumerate(response['songs']):
            # print(num)
            song_dict = {}
            singer_dict = {}
            song_dict["num"] = str(num)
            song_dict["name"] = song['name']

            singer_dict["id"] = ''
            singer_dict["name"] = song['ar'][0]['name']
            singer_dict["age"] = 0
            singer_dict["nation"] = ''

            song_dict["singer"] = singer_dict
            song_dict["picture"] = pic_url
            song_dict["link"] = mus_url
            song_list.append(song_dict)
        return song_list

    def get_mp3(self, id):
        d = '{"ids":"[%s]","br":320000,"csrf_token":""}' % id
        wyy = AesDecode(d)
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        # print(response)
        return response['data'][0]['url']

    def __download_mp3(self, url, filename):
        """下载mp3"""
        abspath = os.path.abspath('.')  # 获取绝对路径
        mac_path = './down_music'
        os.chdir(abspath)
        response = requests.get(url, headers=self.headers).content
        path = os.path.join(mac_path, filename)
        path = path + '.mp3'

        with open(path, 'wb') as f:
            f.write(response)
            print('歌曲下载完毕,可以在{0}路径下查看'.format(path))
        return path

    def down_picture(self, url, filename):
        path = './down_picture/'
        response = requests.get(url, headers=self.headers).content
        with open(path + '.jpg', 'wb') as f:
            f.write(response)
            print('专辑封面下载完毕,可以在%s 路径下查看' % path)
        return path

    def __print_info(self, songs):
        """打印歌曲需要下载的歌曲信息"""
        songs_list = []
        for num, song in enumerate(songs):
            print(num, '歌曲名字：', song['name'], '作者：', song['ar'][0]['name'])
            songs_list.append((song['name'], song['id']))
        return songs_list

    def run(self):
        name = input('请输入你需要下载的歌曲：')
        songs = self.get_songs(name)['result']
        pic_url = songs['songs'][0]['al']['picUrl']
        if songs['songCount'] == 0:
            print('没有搜到此歌曲，请换个关键字')
        else:
            songs = self.__print_info(songs['songs'])
            num = input('请输入需要下载的歌曲，输入左边对应数字即可')
            url = self.get_mp3(songs[int(num)][1])

            if not url:
                print('歌曲需要收费，下载失败')
            else:
                filename = songs[int(num)][0]
                path = self.__download_mp3(url, filename)
                ufile_up.put_file(path, filename)
                # self.down_picture(pic_url, filename) #下载专辑封面


class AesDecode(object):
    def __init__(self, d):
        self.d = d
        self.e = '010001'
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5a" \
                 "a76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46be" \
                 "e255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = "0CoJUm6Qyw8W8jud"
        self.random_text = self.get_random_str()

    def get_random_str(self):
        """js中的a函数"""
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for x in range(16):
            index = math.floor(random.random() * len(str))
            res += str[index]
        return res

    def aes_encrypt(self, text, key):
        iv = b'0102030405060708'  # 偏移量
        pad = 16 - len(text.encode()) % 16  # 使加密信息的长度为16的倍数，要不会报下面的错
        # 长度是16的倍数还会报错，不能包含中文，要对他进行unicode编码
        # Input strings must be a multiple of 16 in length
        text = text + pad * chr(pad)
        # print(iv, type(iv))
        new_key = key.encode('utf-8')
        # 测试新版本key类型 字符串——> 二进制(decoded)
        # print(key, type(key))
        # print(key, type(new_key))

        encryptor = AES.new(new_key, AES.MODE_CBC, iv)
        msg = base64.b64encode(encryptor.encrypt(
            text.encode('utf-8')))  # 最后还需要使用base64进行加密
        return msg

    def rsa_encrypt(self, value, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'),
                 16) ** int(value, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_data(self):
        # 这个参数加密两次
        params = self.aes_encrypt(self.d, self.g)
        params = self.aes_encrypt(params.decode('utf-8'), self.random_text)
        enc_sec_key = self.rsa_encrypt(self.e, self.random_text, self.f)
        return {
            'params': params,
            'encSecKey': enc_sec_key
        }


def main():
    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()

