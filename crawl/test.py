import requests

headers = {
    "Cookie":"_gscu_2116842793=620715794h0w4w15; _gscbrs_2116842793=1; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1562071581; wzws_cid=e8944f2ac5ee47493fb4bc6f983325fd07f721d77e58e06becacfe4e2b2cc6caa80d4432cd54628c413ec56b8fb6ee492aae9d022fd2f668ef9a678e3f7a339d; ASP.NET_SessionId=frms5jm3x10vqnh4o3uy5xwx; VCode=9728a022-2328-4c5a-b079-44d6f365321a; vjkl5=9280072994ff0eb3db019618ab2760445dbfc78e; _gscs_2116842793=t62077095inltbs15|pv:4; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1562077195",
    "Host":"wenshu.court.gov.cn",
    "Pragma":"no-cache",
"Referer":"http://wenshu.court.gov.cn/content/content?DocID=029bb843-b458-4d1c-8928-fe80da403cfe&KeyWord=",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}

sess = requests.session()

sess.headers = headers

response = sess.get("http://wenshu.court.gov.cn//CreateContentJS/CreateContentJS.aspx?DocID=")

print(response.text)