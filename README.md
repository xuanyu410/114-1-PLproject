# 114-1 程式語言期末專題
[專題提案影片連結](https://youtu.be/x1fED5DUDnU)
## 你觀星嗎?
### 核心問題
1. 缺乏入門指引，難以踏入觀星領域
2. 看到星星卻不知道名稱與星座，缺少即時辨識工具
2. 缺乏方便的觀星紀錄方式，無法隨時建立日誌
### 目標
1. 天頂星座定位：整合 Folium 地圖與 Google Gemini AI。用戶點擊地圖位置後，系統自動抓取經緯度與當前時間，推算當下的天頂星座及其神話背景。
2. 星空模擬圖：嵌入 VirtualSky 互動式星圖，提供即時的天體視覺化，支援星座連線、亮星標籤與座標網格切換。
3. AI 天文問答：串接 Gemini 2.5 Flash 模型，針對用戶的天文疑問提供專業、即時的繁體中文解答。
4. 天文論壇爬蟲：自動爬取 Astronomy.com 最新文章，透過 BeautifulSoup 抓取標題，並利用 jieba 分詞與 WordCloud 產生熱門話題文字雲。
5. 觀星日誌：使用 Google Sheets 作為資料庫，支援觀測數據（時間、地點、天氣、器材、評分）的儲存、顯示與刪除，並整合 Catbox API 實現觀星照片上傳。
### 技術架構
- 前端框架：Streamlit (Python)
- AI 模型：Google Gemini 2.5 Flash
- 地圖組件：Folium, streamlit-folium
- 數據儲存：Google Sheets API (gspread)
- 爬蟲與分析：Requests, BeautifulSoup, WordCloud, jieba
- 部署工具：ngrok (用於 Colab 環境啟動)
### 程式碼結構簡述
- app.py: 主程式邏輯，包含多分頁導覽系統。
- connect_to_gsheet(): 處理 Google Sheets 認證與連線。
- upload_to_catbox(): 將觀星照片上傳至 Catbox 伺服器並回傳網址。
- CSS Styles: 自定義深藍色星空主題，優化 UI/UX 體驗。
### 成果效益與價值
1. 降低觀星入門門檻，提升大眾參與度
2. 建立一站式的觀星平台，提高使用體驗的一致性
3. 提升使用者在真實夜空中的辨識能力
4. 讓觀星從一次性的體驗變成可累積的學習過程
### 未來展望
1. 將專案開發成app讓使用者方便下載
2. 加入 AI 圖像辨識：對著夜空拍照即可辨識星體
3. 結合天文觀測站 API（ISS、流星雨、彗星預報）
