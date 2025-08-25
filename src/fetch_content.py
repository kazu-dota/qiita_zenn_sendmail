import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_article_content(url: str) -> str:
    """
    指定されたURLから記事の本文を取得する
    
    Args:
        url (str): 記事のURL
        
    Returns:
        str: 記事の本文テキスト
    """
    try:
        # リクエストヘッダーを設定（ブロック対策）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # サイトごとに異なる記事本文の取得方法
        if 'qiita.com' in url:
            content = extract_qiita_content(soup)
        elif 'zenn.dev' in url:
            content = extract_zenn_content(soup)
        else:
            # 一般的なWebページの場合
            content = extract_general_content(soup)
        
        return content if content else "記事の内容を取得できませんでした。"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"URL {url} の取得でネットワークエラー: {e}")
        return f"記事の取得中にネットワークエラーが発生しました: {e}"
    except Exception as e:
        logger.error(f"URL {url} の処理中にエラー: {e}")
        return f"記事の処理中にエラーが発生しました: {e}"

def extract_qiita_content(soup: BeautifulSoup) -> str:
    """Qiitaの記事本文を抽出"""
    # Qiitaの記事本文は通常 .it-MdContent クラスまたは類似のクラス内にある
    content_selectors = [
        '.it-MdContent',
        '.md-content',
        '[data-testid="article-body"]',
        '.article-body'
    ]
    
    for selector in content_selectors:
        content_div = soup.select_one(selector)
        if content_div:
            # HTMLタグを除去してテキストのみを取得
            text = content_div.get_text(strip=True, separator='\n')
            # 長すぎる場合は前半部分のみを取得（要約時のトークン制限対策）
            return text[:2000] if len(text) > 2000 else text
    
    return ""

def extract_zenn_content(soup: BeautifulSoup) -> str:
    """Zennの記事本文を抽出"""
    # Zennの記事本文は通常 .znc または類似のクラス内にある
    content_selectors = [
        '.znc',
        '.markdown-body',
        '[data-testid="article-body"]',
        '.article-body'
    ]
    
    for selector in content_selectors:
        content_div = soup.select_one(selector)
        if content_div:
            text = content_div.get_text(strip=True, separator='\n')
            return text[:2000] if len(text) > 2000 else text
    
    return ""

def extract_general_content(soup: BeautifulSoup) -> str:
    """一般的なWebページの本文を抽出"""
    # 一般的な記事本文のセレクタ
    content_selectors = [
        'article',
        '.content',
        '.post-content',
        '.entry-content',
        'main',
        '.main-content'
    ]
    
    for selector in content_selectors:
        content_div = soup.select_one(selector)
        if content_div:
            text = content_div.get_text(strip=True, separator='\n')
            return text[:2000] if len(text) > 2000 else text
    
    # フォールバック: body全体から不要な部分を除去
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.decompose()
    
    text = soup.get_text(strip=True, separator='\n')
    return text[:2000] if len(text) > 2000 else text

def fetch_articles_content(articles: List[Dict[str, str]], max_articles: int = 5) -> List[Dict[str, str]]:
    """
    複数の記事の内容を取得する
    
    Args:
        articles (List[Dict]): 記事情報のリスト（title, linkを含む）
        max_articles (int): 処理する記事の最大数
        
    Returns:
        List[Dict]: 記事情報に内容を追加したリスト
    """
    enriched_articles = []
    
    for i, article in enumerate(articles[:max_articles]):
        logger.info(f"記事 {i+1}/{min(len(articles), max_articles)} を処理中: {article['title']}")
        
        # 記事内容を取得
        content = fetch_article_content(article['link'])
        
        # 記事情報に内容を追加
        enriched_articles.append({
            'title': article['title'],
            'link': article['link'],
            'content': content
        })
        
        # レート制限対策
        time.sleep(1)
    
    return enriched_articles

if __name__ == "__main__":
    # テスト用
    test_articles = [
        {
            "title": "テスト記事",
            "link": "https://qiita.com/trending"
        }
    ]
    
    result = fetch_articles_content(test_articles, 1)
    for article in result:
        print(f"タイトル: {article['title']}")
        print(f"URL: {article['link']}")
        print(f"内容: {article['content'][:200]}...")