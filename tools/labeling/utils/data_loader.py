"""
data_loader.py - 支持从在线《资治通鉴》网站批量抓取章节文本
"""
import requests
from bs4 import BeautifulSoup

class DataLoader:
    @staticmethod
    def fetch_chapter_urls(index_url: str) -> list:
        """抓取目录页所有章节的URL"""
        resp = requests.get(index_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 假设章节链接在a标签且包含“卷”字，可根据实际页面结构调整
        links = soup.find_all('a', href=True)
        chapter_urls = [link['href'] for link in links if '卷' in link.text or '纪' in link.text]
        # 补全为绝对路径
        chapter_urls = [url if url.startswith('http') else requests.compat.urljoin(index_url, url) for url in chapter_urls]
        return chapter_urls

    @staticmethod
    def fetch_chapter_text(chapter_url: str) -> str:
        """抓取单个章节正文文本"""
        resp = requests.get(chapter_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 假设正文在id/class为content/main的div，可根据实际页面结构调整
        content = soup.find('div', {'id': 'content'}) or soup.find('div', {'class': 'main'})
        if content:
            text = content.get_text(separator='\n', strip=True)
        else:
            # 兜底：抓取所有<p>
            ps = soup.find_all('p')
            text = '\n'.join([p.get_text(strip=True) for p in ps])
        return text

    @staticmethod
    def fetch_all_chapters(index_url: str) -> list:
        """批量抓取所有章节文本，返回[{title, url, text}]"""
        chapters = []
        urls = DataLoader.fetch_chapter_urls(index_url)
        for url in urls:
            print(f"[INFO] 抓取章节: {url}")
            text = DataLoader.fetch_chapter_text(url)
            title = url.split('/')[-1]
            chapters.append({'title': title, 'url': url, 'text': text})
        return chapters

    @staticmethod
    def to_llm_format(chapters: list) -> list:
        """将章节列表转换为LLM可批量抽取的格式（如每章一段）"""
        return [ch['text'] for ch in chapters if ch['text'].strip()]