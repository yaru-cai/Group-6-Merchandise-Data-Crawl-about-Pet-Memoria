import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of city codes 
city_codes = ['1', '2', '7', '4','9','6','8','3','16','5','10']
all_shops = []


# Headers for the request
headers = {
    'cookie': '_lxsdk_cuid=192f70eacc4c8-0968767bb4c92e-4c657b58-1bcab9-192f70eacc4c8; _lxsdk=192f70eacc4c8-0968767bb4c92e-4c657b58-1bcab9-192f70eacc4c8; _hc.v=a1cbafa3-1add-29d7-74ea-9cd2967048e0.1730721787; s_ViewType=10; WEBDFPID=xy7652988zxy5vv21x1yvy5x73x0718z807u29vww4z97958yyxwyu7v-2046081799091-1730721797666MEOEKSYfd79fef3d01d5e9aadc18ccd4d0c95071046; ctu=d8fff290c4a24d4923f4a50f3b0dcf299066b0d3920a2fef39efcb0d53356683; cy=2; cye=beijing; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1731154471,1731213346,1732251718,1733461450; HMACCOUNT=9037DADD046FCA7B; logan_session_token=bo38ij7fznejkp3rddac; qruuid=730673ab-99dd-48f9-bba0-a33c88096d8a; dplet=7edf793b85568e04911c3964b80fe051; dper=020224235bc959cb34d9ab0ad20d4d0703e7c855b9752b6eb877bd4a2c45d18056853049cb4f0a5b6a7d10339f3a6dbf0ab79536294a9699b15700000000f9240000db77d9b2ca87c2d55208c4044bb9f06b435f92481759f6501bf6d64cd6ef89e2b383831ab4f1e169906dc691b0176222; ll=7fd06e815b796be3df069dec7836c3df; ua=%E8%8A%A6%E7%AC%8B%E6%B6%AE%E6%A9%84%E6%A6%84%E6%B2%B9; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1733462444; _lxsdk_s=1939a5a0548-cf8-a28-9a%7C%7C163',
    'host': 'www.dianping.com',
    'referer': 'https://www.dianping.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

for city_code in city_codes:
    url = f'https://www.dianping.com/search/keyword/{city_code}/0_%E5%AE%A0%E7%89%A9%E6%AE%A1%E8%91%AC'
    page_source = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page_source.text, 'html.parser')
    page_info = soup.find("div", class_="page")

    if page_info:
        pages = page_info.find_all("a")
        total_pages = int(pages[-2].get_text())
    else:
        total_pages = 1

    print(f"城市代码 {city_code} 的总页数: {total_pages}")

    # 存储所有标题、规模、评价数、价格、地址
    names = []
    scale = []
    review = []
    prices = []
    location = []

    for page in range(1, total_pages + 1):
        url_with_page = f'{url}/p{page}'
        page_source = requests.get(url=url_with_page, headers=headers)
        soup = BeautifulSoup(page_source.text, 'html.parser')
        shop_list_div = soup.find("div", id="shop-all-list")
        shops = shop_list_div.find_all('li') if shop_list_div else []

        for shop in shops:
            h4_tag = shop.find('h4')
            names.append(h4_tag.get_text() if h4_tag else "无")

            scale_tag = shop.find('a', class_="shop-branch")
            scale.append("有" if scale_tag and scale_tag.get_text(strip=True) else "无")

            review_tag = shop.find('a', class_="review-num")
            review_b = review_tag.find('b') if review_tag else None
            review.append(review_b.get_text() if review_b else "无")

            price_tag = shop.find('a', class_="mean-price")
            price_b = price_tag.find('b') if price_tag else None
            prices.append(price_b.get_text() if price_b else "未知")

            location_tag = shop.find('a', {'data-click-name': 'shop_tag_region_click'})
            location.append(location_tag.get_text() if location_tag else "无")

        print(f"城市代码 {city_code} 的第 {page} 页已爬取完毕")

    # 打印数据
    for name, branch, reviews, price, loc in zip(names, scale, review, prices, location):
        print(f"城市代码:{city_code}, 店名: {name}, 分店: {branch}, 评价数: {reviews}, 价格: {price}, 地址: {loc}")

    # 将数据添加到总列表
    for i in range(len(names)):
        all_shops.append((city_code, names[i], scale[i], review[i], prices[i], location[i]))

# 将所有数据转换为 DataFrame
df = pd.DataFrame(all_shops, columns=['城市代码', '店名', '分店', '评价数', '价格', '地址'])

# 输出数据到CSV
df.to_csv('12072.csv', encoding='utf-8-sig', index=False)
print("数据已保存到 12072.csv")

