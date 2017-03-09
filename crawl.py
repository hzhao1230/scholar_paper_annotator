# May 18, 2016. He Zhao
# Journals include:
# IEEE proceedings
# Elsevier: Composite science and technology
# ACS

from scholar import *
from scholar_publishers import *
from urllib import urlretrieve
import pandas as pd
import time
import csv
from itertools import izip
import random

def crawl(query_key_words, num_query_results):
    # Apply google scholar querier
    querier = ScholarQuerier()
    settings = ScholarSettings()
    querier.apply_settings(settings)
    query = SearchScholarQuery()
    query.phrase = query_key_words
    query.set_num_page_results(num_query_results)
    querier.send_query(query)
    articles = querier.articles

    print 'The number of articles returned',len(articles)
    
    list_query_result = {}
    url=[]
    # Determine publisher from URL
    # Parse DOI or article number from returned url from google scholar search
    for article in articles:
        title = article.attrs['title'][0]
        url = article.attrs['url'][0]
        #print url,len(url)
        publisher = '' # default: no match with existing publisher 
        if str(url).strip('http://').split('/')[0] == 'ieeexplore.ieee.org':
        # if str(url).split('=')[0] == 'http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber':
            publisher = 'ieee'
            # article_num = str(url).split('=')[1]
            article_num = str(url).strip('http://').split('/')[-1]
        elif str(url).split('/')[2] == 'www.sciencedirect.com':
            publisher = 'ScienceDirect'
            article_num = str(url).split('/')[6]
        elif str(url).split('/')[2] == 'pubs.acs.org':
            publisher = 'acs'
            article_num = str(url).split('/')[-1]
        ### 03/07/17 Yixing updated aip
        elif str(url).split('/')[2] == 'aip.scitation.org':
            publisher = 'aip'
            article_num = str(url).split('/')[-1]
            print article_num

        elif str(url).split('/')[2] == 'pubs.rsc.org':
            publisher = 'rsc'
            words = str(url).split('/')[-3:]
            article_num = ''
            for word in words:
                article_num += word+'_'
            article_num = article_num[:-1]
        if publisher != '':
            if publisher in list_query_result:
                list_query_result[publisher].append(article_num)
            else:
                list_query_result[publisher] = [article_num]
    
    
    for publisher in list_query_result.keys():
        if publisher == 'ieee':
            prefix = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber='
            # for each paper belonging to a publisher
            for i in xrange(len(list_query_result[publisher])):
                article_num = list_query_result[publisher][i]
                paper_url = prefix + str(article_num)
                print paper_url
                # initialize crawler
                crawler = ieee(paper_url)
                # Create new folder for the paper if not existed
                paper_dir = './'+publisher+'/'+str(article_num)+'/'
                if not os.path.exists(paper_dir):
                    os.makedirs(paper_dir)
                # Get list of urls for images
                img_list = crawler.get_img_url()
                print len(img_list)
                print img_list
                # Download all images to paper folder
                crawler.download_img(img_list, paper_dir)
                # Get title and abstract of the paper and write to the paper folder
                title, abstract = crawler.get_title_abstract()

                # 030317 add main body
                main_body_text = crawler.get_main_body()

                title_file = open(paper_dir+'title.txt', "w")
                title_file.write(title)
                title_file.close()
                abstract_file = open(paper_dir+'abstract.txt', "w")
                abstract_file.write(abstract)
                abstract_file.close()
                # Close browser
                crawler.close_browser()
            
        elif publisher == 'ScienceDirect':
            prefix = 'http://www.sciencedirect.com/science/article/pii/'
            # for each paper belonging to a publisher
            for i in xrange(len(list_query_result[publisher])):
                article_num = list_query_result[publisher][i]
                paper_url = prefix + str(article_num)
                print paper_url
                # initialize crawler
                crawler = ScienceDirect(paper_url)
                # Create new folder for the paper if not existed
                paper_dir = './'+publisher+'/'+str(article_num)+'/'
                print paper_dir
                if not os.path.exists(paper_dir):
                    os.makedirs(paper_dir)
                # Get list of urls for images
                img_list = crawler.get_img_url()
                print len(img_list)
                print img_list
                # Download all images to paper folder
                crawler.download_img(img_list, paper_dir)
                # Get title and abstract of the paper and write to the paper folder
                title, abstract = crawler.get_title_abstract()
                title_file = open(paper_dir+'title.txt', "w")
                title_file.write(title)
                title_file.close()
                abstract_file = open(paper_dir+'abstract.txt', "w")
                abstract_file.write(abstract)
                abstract_file.close()
                # Close browser
                crawler.close_browser()
        
        elif publisher == 'acs':
            prefix = 'http://pubs.acs.org/doi/full/10.1021/'
            # for each paper belonging to a publisher
            for i in xrange(len(list_query_result[publisher])):
                article_num = list_query_result[publisher][i]
                paper_url = prefix + str(article_num)
                print paper_url
                # initialize crawler
                crawler = acs(paper_url)
                # Create new folder for the paper if not existed
                paper_dir = './'+publisher+'/'+str(article_num)+'/'
                print paper_dir
                if not os.path.exists(paper_dir):
                    os.makedirs(paper_dir)
                # Get list of urls for images
                img_list = crawler.get_img_url()
                print len(img_list)
                print img_list
                # Download all images to paper folder
                crawler.download_img(img_list, paper_dir)
                # Get title and abstract of the paper and write to the paper folder
                title, abstract = crawler.get_title_abstract()
                title_file = open(paper_dir+'title.txt', "w")
                title_file.write(title)
                title_file.close()
                abstract_file = open(paper_dir+'abstract.txt', "w")
                abstract_file.write(abstract)
                abstract_file.close()
                # Close browser
                crawler.close_browser()
        elif publisher == 'aip':
            # STILL WORKING ON THIS  update by Yixing
            prefix = 'http://aip.scitation.org/doi/full/10.1063/'
            # for each paper belonging to a publisher
            for i in xrange(len(list_query_result[publisher])):
                article_num = list_query_result[publisher][i]
                paper_url = prefix + str(article_num)
                print paper_url
                # initialize crawler
                crawler = aip(paper_url)
                # Create new folder for the paper if not existed
                paper_dir = './'+publisher+'/'+str(article_num)+'/'
                print paper_dir
                if not os.path.exists(paper_dir):
                    os.makedirs(paper_dir)
                # Get title and abstract of the paper and write to the paper folder
                title, abstract = crawler.get_title_abstract()
                title_file = open(paper_dir+'title.txt', "w")
                title_file.write(title)
                title_file.close()
                abstract_file = open(paper_dir+'abstract.txt', "w")
                abstract_file.write(abstract)
                abstract_file.close()
                # Close browser
                crawler.close_browser()                    
            pass
        elif publisher == 'rsc':
            prefix = 'http://pubs.rsc.org/en/content/articlehtml/'
            for i in xrange(len(list_query_result[publisher])): 
                article_num = list_query_result[publisher][i]
                words = article_num.split('_')
                sub_url_str = ''
                for word in words:
                    sub_url_str += word+'/'
                paper_url = prefix + sub_url_str
                print paper_url
                # initialize crawler
                crawler = rsc(paper_url)
                # Create new folder for the paper if not existed
                paper_dir = './'+publisher+'/'+str(article_num)+'/'
                print paper_dir
                if not os.path.exists(paper_dir):
                    os.makedirs(paper_dir)                
                title, abstract = crawler.get_title_abstract()
                title_file = open(paper_dir+'title.txt', "w")
                title_file.write(title)
                title_file.close()
                abstract_file = open(paper_dir+'abstract.txt', "w")
                abstract_file.write(abstract)
                abstract_file.close()
                # Close browser
                crawler.close_browser()

    return 'NO link found' if len(url)==0 else url 


if __name__=='__main__':
    doi_df = pd.read_csv('doi_list1.csv', header=None)
    urllist=[]
    doilist=[]
    for i in range(doi_df.shape[0]):
        query_key_words = doi_df.iloc[i][0]
        doilist.append(query_key_words)
        print query_key_words
    # query_key_words = 'polymer nanodielectric'
        num_query_results = 1 
        timestop=random.random()*30+30
        print "The stopping time is",timestop

        time.sleep(timestop)
        url=crawl(query_key_words, num_query_results)
        print url
        urllist.append(url)
    ##write url to a csvfile
    with open('url.csv','wb') as f:
        writer=csv.writer(f)
        writer.writerows(izip(doilist,urllist))


    
    # query_key_words ='10.1016/j.compscitech.2007.05.021'
    # num_query_results = 1

    # url=crawl(query_key_words, num_query_results)
    # print url
