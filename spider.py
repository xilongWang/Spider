# -*- coding: utf-8 -*-
import requests
import os
import codecs
import time
import multiprocessing
from bs4 import BeautifulSoup
headers={
    "Accept":"text/html",
    "Accept-Charset":"utf-8",
    "Accept-Language":"zh-CN,zh",
    "Accept-Encoding":"gzip",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko)\
     Chrome/25.0.1364.160 Safari/537.22"
        }
save_path='D:\\voc_image\\'
base_url = 'http://www.xiurr.com/page/'
j=1
has_get=[]
def main(i,j):
    id=os.getpid()
    url=base_url+str(i)
    print url
    html=requests.get(url,headers=headers).content
    soup=BeautifulSoup(html,'html.parser')
    img_url=soup.find_all('img')
    #print '#'*20
    for image in img_url:
        #print image
        if image.has_attr('data-lazy-src') and image.has_attr('alt'):

            #print image
            title=image.get('alt')
            #print title
            title=title.strip().replace(' ','').replace(u'？','').replace('?','')\
                 .replace('!','').replace('*','')
            img_link=image.get('data-lazy-src').encode('utf-8')
            #print title,img_link
            #print title,id
            print img_link
            ii=img_link[-4:]
            if (ii=='.jpg'or ii=='gif') and not (title.endswith('jpg') or title.endswith('.gif')):

                has_get.append(str(img_link))
                cont=requests.get(img_link,headers=headers).content
                with codecs.open(save_path+title+ii,'wb') as f:
                    f.write(cont)
                    print 'From page %d Downloading the %d picyure ProcessID %s' % (i,j,id)
                    print '\n'
                    j+=1
                    if j%30==0:
                        time.sleep(3)

if __name__=="__main__":
    start_time=time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(1,865):
        pool.apply_async(main,(i,j))#注意，子进程中的print，这里如果不传j，main函数中的 print 'From
                                    # page %d Downloading the %d picyure ProcessID %s' % (i,j,id)打印不出来
    pool.close()
    pool.join()
    Use_time=time.time()-start_time
    print 'Use %5d second'% Use_time
