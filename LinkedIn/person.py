from turtle import title
from LinkedIn.modules import *

class Person:
    def __init__(self, browser, url, delay=10):
        self._browser = browser
        self._url = url
        self._delay = delay
        browser.get(url)

    @property
    def name(self) -> str|None:
        soup = BeautifulSoup(self._browser.page_source, 'lxml')
        pname = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})
        if pname is not None:
            return pname.text.strip()
        return pname

    @property
    def address(self) -> str|None:
        soup = BeautifulSoup(self._browser.page_source, 'lxml')
        padd = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})
        if padd is not None:
            return padd.text.strip()
        return padd

    def _urljoin(self, curr_url, suburl):
        return curr_url.strip('/') + suburl
    
    def experiences(self) -> list:
        self._browser.get(self._url)
        curr_url = self._browser.current_url
        exp_url = self._urljoin(curr_url, '/details/experience/')
        self._browser.get(exp_url)
        job_titles = []
        
        WebDriverWait(self._browser, self._delay).until(EC.presence_of_element_located((By.XPATH, "//span[@class='mr1 t-bold']")))
        
        soup = BeautifulSoup(self._browser.page_source, 'lxml')
        ul = soup.find('ul', {'class': 'pvs-list'})
        
        if ul is not None:
            lis = ul.find_all('li')
            for li in lis:

                datas = {
                    'Job Title': None,
                    'Tenure': None,
                    'Company Name': None,
                }

                title, tenure, company = None, None, None
                span = li.find('span', {'class': 'mr1 t-bold'})

                if span is None:
                    continue
   
                title = span.find('span').get_text()
                company = str(span.parent.find_next_sibling('span').get_text()).strip()

                for span in li.find_all('span'):
                    if re.search('[0-9]+ mos?', str(span.get_text())):
                        tenure = span.find('span', {'class': 'visually-hidden'}).get_text().strip()
                        break

                if title is not None and tenure is not None:
                    datas['Job Title'] = title
                    datas['Tenure'] = tenure
                    datas['Company Name'] = company

                job_titles.append(datas)

        return job_titles