import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR



def task1_task2():
    # To show that the crawler has started
    print('Started')

#### TASK 1:
    # chromedriver to add the path of the chromedriver
    chromedriver = 'C:\WebDriver\chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    # Driver is used to reach the website
    driver.get('http://quote.eastmoney.com/center/boardlist.html#concept_board')

    # Initialize the dataframe
    allData =[]

    # While loop to reach the end of the page
    while (True):

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Rows contains all the rows present in the table from the particular page
        rows = soup.select('table tbody tr')

        for r in rows:
            # Find all the data items from the row
            td = r.find_all('td')
            # Append all the values present in the row
            row = [i.text for i in td]
            # Find all the children of data items in row with tag 'a'
            links = td[2].findChildren('a')
            # Add only the href present in the column sector_name
            row.append(links[len(links)-1]['href'])
            # Append the row in allData which contains all the data
            allData.append(row)

        # When we reach the last page of the table end the loop when the 'Next Page' button is disabled.
        if driver.find_element_by_xpath('//*[@id="main-table_paginate"]/a[2]').get_attribute('class') == 'next paginate_button disabled':
            break

        # Click the 'Next Page' button
        driver.find_element_by_xpath('//a[@class= "next paginate_button"]').click()

        # To let the page load
        time.sleep(1)

    # DataFrame which contains all the data with new column names
    d = pd.DataFrame(allData, columns=['ranking','sector_name','related_link','price_close','price_change','price_change_pct','total_market_cap','turnover_rate','num_of_company_up','num_of_company_down','down_company','price_change_pct_down','hyperlink'])

    # DataFrame which contains only sector_name and total_market_cap
    d1 = d.drop(columns = ['ranking','related_link','price_close','price_change','price_change_pct','turnover_rate','num_of_company_up','num_of_company_down','down_company','price_change_pct_down','hyperlink'])

    print('Data Frame Containing all the data from the table with new column names',d)
    print('Data Frame after dropping all columns except for sector_name and total_market_cap',d1)


#### TASK 2:


    # Credentials of the connection
    hostname = "LAPTOP-3A8RPR2F"
    db = "investbots"
    un = "investbots"
    pw = "majumdar22"

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=db, user=un, pw=pw))

    # Add all the values of df1 to the table which contains the sector_name and total_market_cap.
    d1.to_sql('datas', engine, dtype={"sector_name": VARCHAR(20), "total_market_cap": VARCHAR(20)})
    # Assign sector_name as the primary key
    engine.execute('ALTER TABLE datas ADD PRIMARY KEY (`sector_name`);')

    driver.close()

# Main Function
if __name__ == '__main__':
    task1_task2()