#/usr/bin/python3

import zlib

import urllib.request
import urllib.error
import urllib

from bs4 import BeautifulSoup
import urllib3

def create_header():
	head = urllib3.util.make_headers(keep_alive=True, accept_encoding="gzip, deflate", user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36', basic_auth=None)
	head['Host'] = 'www.gxlawyer.org.cn'
	head['Cache-Control'] = 'max-age=0'
	head['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	head['Referer'] = 'http://www.gxlawyer.org.cn'
	head['Accept-Encoding'] = 'gzip, deflate'
	head['Accept-Language'] = 'zh-CN,zh;q=0.8'

	return head

def create_body(page_id):
	data = 'currentPage=' + repr(page_id)
	return data

def track_info(tbody, fp):
	for lsss in tbody:
		#print(lsss.dl.dt.h3.a.string)
		laws_f = lsss.find('table')
		if not laws_f: continue
		laws = laws_f.findAll('a')
		for law in laws:
			fp.write("%s %s http://www.gxlawyer.org.cn%s\n" %(law.string, lsss.dl.dt.h3.a.string, law.get('href')))
	return	
	
	
if __name__ == "__main__":
	
	url = 'http://www.gxlawyer.org.cn/searchLawFirm?page='	
	result_file = 'guangxi_law.txt'	
	
	fp = open(result_file, 'w')
	header = create_header()
	
	page_id = 1
	while True:
		print("Current page: %d" % page_id)
		body = create_body(page_id)
		req = urllib.request.Request(url+repr(page_id), headers=header)
		response = urllib.request.urlopen(req)
		if response.info().get('Content-Encoding') == 'gzip':
			r_read = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
		else:    
			r_read = response.read()
		soup = BeautifulSoup(r_read.decode('utf-8'), 'lxml')
		info_soup = soup.findAll('div', attrs={"class":"intro"})
		if info_soup:
			track_info(info_soup, fp)
		
		page_id += 1
		if page_id > 61:
			break
	
	fp.close()
	print("Done!")
