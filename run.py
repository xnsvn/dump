import requests
import bs4
import re
import sys
import os
os.system('clear')
print(40*'-')
parser = bs4.BeautifulSoup
ses = requests.Session()

cookie = ""#masukan kuki

cok = {"cookie": cookie}


def main():
    user = input(" Put Public ID: ")
    print(40*'-')
    file = input(' File save location: ')
    print (40*'-')
    cek(user)
    dump_publik(f"https://mbasic.facebook.com/{user}/friends",file)


def cek(user):
    try:
        link = ses.get(f"https://mbasic.facebook.com/{user}/friends", cookies=cok).text
        if "Tidak Ada Teman Untuk Ditampilkan" in link:
            exit("Private friends")
        elif "Halaman yang Anda minta tidak ditemukan." in link:
            exit("Target not found")
        elif "Anda Tidak Dapat Menggunakan Fitur Ini Sekarang" in link:
            exit("Limited function")
        elif "Konten Tidak Ditemukan" in link:
            exit("Target not found")
        else:
            pass
    except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ReadTimeout):
        exit("[!] Connection error")


def dump_publik(url,file):
    try:
        headers = {
            "Host": "mbasic.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="106"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.126 Mobile Safari/537.36 OPR/72.4.3767.69265",
            "cookie": cok["cookie"],
        }
        link = ses.get(url, headers=headers).text
        data = re.findall('middle"><a class=".." href="(.*?)">(.*?)</a>', link)
      #  print(data)
        for user in data:
            if "profile.php?" in user[0]:
                mentah = re.findall("id=(.*?)&", user[0])[0] + "|" + user[1]
                open(file, "a").write(str(mentah) + "\n")
                xxx = open(file, "r").read().splitlines()
                sys.stdout.write(f'\r\r\033[1;37m Collecting ids :- {str(len(xxx))}');sys.stdout.flush()
              #  input()
            else:
                pass

        if "See more friends" in link:
            #print(" Have More Friends")
            file = "/sdcard/dump/file.txt"
            dump_publik("https://mbasic.facebook.com" + parser(link, "html.parser").find("a", string="See more friends").get("href"),file)
    except Exception as e:
        print(e)




main()