import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from collections import Counter
import re
import jieba
import time
import gspread
from PIL import Image
import io
import base64
import os
import google.generativeai as genai
import requests
import pytz  # 🟢 新增：導入時區處理套件
from google.oauth2.service_account import Credentials

# CSS 樣式 (此部分保持不變)
st.markdown("""
    <style>
    .main {
        background-color: #0a0e27;
        color: #f5f5dc;
    }
    .stApp {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
    }
    h1, h2, h3 {
        color: #64b5f6 !important;
    }
    p, .stMarkdown, .stText, label, .stCheckbox label {
        color: #f5f5dc !important;
    }
    .stButton>button {
        background-color: #1976d2;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1565c0;
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(100, 181, 246, 0.5);
    }
    /* Sidebar 樣式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #2a2f4a 100%);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] h1 {
        color: #64b5f6 !important;
    }
    [data-testid="stSidebar"] .stRadio > label {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: #e0e0e0 !important;
    }

    /* 首頁動畫樣式 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    .home-title {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #64b5f6, #90caf9, #bbdefb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 2s ease-out, float 3s ease-in-out infinite;
        margin: 2rem 0;
    }
    .home-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #90caf9;
        animation: fadeIn 2.5s ease-out;
        margin-bottom: 3rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #64b5f6;
        animation: fadeIn 3s ease-out;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(100, 181, 246, 0.4);
        border-color: #90caf9;
    }
    .feature-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        animation: twinkle 2s ease-in-out infinite;
    }
    .feature-title {
        font-size: 1.5rem;
        color: #64b5f6;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #e0e0e0;
        text-align: center;
        font-size: 1rem;
    }
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s ease-in-out infinite;
    }

    /* 外框 */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    /* 輸入框本體 */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 10px;
        border: 1px solid #64b5f6;
        font-size: 1rem;
    }

    /* placeholder 文字 */
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #666666;
    }
    /* focus 時發光（跟你按鈕風格一致） */
    div[data-testid="stChatInput"] textarea:focus {
        outline: none;
        box-shadow: 0 0 15px rgba(100, 181, 246, 0.6);
    }
    div.block-container {
        background-color: #0a0e27;
    }
    /* 最底層（白色真正來源） */
    div[data-testid="stBottom"] {
        background-color: #0a0e27 !important;
    }

    /* Chat input 外層 */
    div[data-testid="stBottom"] > div {
        background-color: #0a0e27 !important;
    }

    /* Chat input 本體 */
    div[data-testid="stChatInput"] {
        background-color: #1a1f3a !important;
    }
    /* 整個 header */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* 右上角工具列 */
    div[data-testid="stToolbar"] {
        background: rgba(10, 14, 39, 0.6) !important;
        backdrop-filter: blur(8px);
        border-radius: 10px;
    }

    /* icon 顏色 */
    div[data-testid="stToolbar"] svg {
        fill: #f5f5dc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 🔑 設定 API Key
# ============================================
try:
    # 嘗試從 secrets.toml 讀取
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    # 使用 st.error 而非 st.exception 以確保輸出更簡潔
    st.error("❌ 未偵測到 API Key！請確認已在 Colab 設定 secrets.toml")
    st.stop()

@st.cache_resource
def connect_to_gsheet():
    try:
        # 設定權限範圍
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 檢查 Secrets
        if "gcp_service_account" not in st.secrets:
            st.error("❌ Secrets 中缺少 [gcp_service_account] 區段")
            return None
            
        # 🟢 正確做法：從 st.secrets 讀取服務帳戶資訊
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], 
            scopes=scopes
        )
        gc = gspread.authorize(creds)
        
        # 使用 ID 開啟
        spreadsheet_id = "1fBthlbG1xhZ2fQna5NYx8Fbj3XbzV0VvXkc93ihZRKw"
        gsheets = gc.open_by_key(spreadsheet_id)
        
        # 檢查工作表名稱 (請確認工作表下方標籤真的叫 "工作表1")
        worksheet = gsheets.worksheet('工作表1')
        return worksheet
        
    except Exception as e:
        # 如果噴 PermissionError，請檢查是否在其他地方有 !mkdir 或 open('...','w')
        st.error(f"❌ Google Sheets 連接失敗: {str(e)}")
        return None
# 初始化連線
worksheet = connect_to_gsheet()
if worksheet:
    init_sheet(worksheet) # 確保表頭存在

# Google Sheets 操作函數 (保持不變)
def load_logs_from_sheet(worksheet):
    try:
        sheets = worksheet.get_all_values()
        if len(sheets) <= 1:
            return []
        df = pd.DataFrame(sheets[1:], columns=sheets[0])
        logs = []
        for _, row in df.iterrows():
            log = {
                "date": row.get("日期", ""),
                "location": row.get("地點", ""),
                "weather": row.get("天氣", ""),
                "constellation": row.get("星座", ""),
                "equipment": row.get("器材", ""),
                "rating": int(row.get("評分", 0)) if row.get("評分", "").isdigit() else 0,
                "notes": row.get("筆記", ""),
                "photo": row.get("照片", "")
            }
            logs.append(log)
        return logs
    except Exception as e:
        st.error(f"❌ 載入資料失敗: {str(e)}")
        return []

def save_log_to_sheet(worksheet, log):
    try:
        row = [
            log["date"],
            log["location"],
            log["weather"],
            log["constellation"],
            log["equipment"],
            str(log["rating"]),
            log["notes"],
            log.get("photo", "")
        ]
        worksheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"❌ 儲存失敗: {str(e)}")
        return False

def init_sheet(worksheet):
    try:
        all_values = worksheet.get_all_values()
        if not all_values or all_values[0][0] != "日期":
            worksheet.clear()
            worksheet.append_row(["日期", "地點", "天氣", "星座", "器材", "評分", "筆記", "照片"])
    except Exception as e:
        st.error(f"❌ 初始化失敗: {str(e)}")

def delete_log_from_sheet(worksheet, sheet_row_index):
    """
    從 Google Sheet 中刪除指定行號的資料。

    :param worksheet: gspread worksheet 物件
    :param sheet_row_index: 要刪除的 Google Sheet 行號 (e.g., 2 代表第二行)
    :return: 成功返回 True，失敗返回 False
    """
    try:
        # worksheet.delete_rows 是 gspread 的函數
        worksheet.delete_rows(sheet_row_index)
        return True
    except Exception as e:
        print(f"Error deleting row from Google Sheet: {e}")
        return False
def upload_to_catbox(file_obj):
    """
    將圖片上傳到 Catbox.moe (免註冊、永久儲存)
    :param file_obj: Streamlit 的 UploadedFile 物件
    :return: 圖片網址 (String) 或 None
    """
    try:
        url = "https://catbox.moe/user/api.php"

        # 準備參數
        data = {'reqtype': 'fileupload'}
        # 讀取檔案二進位資料
        files = {'fileToUpload': file_obj.getvalue()}

        # 發送 POST 請求
        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            # Catbox 直接回傳網址字串，例如 https://files.catbox.moe/xyz.jpg
            return response.text.strip()
        else:
            st.error(f"上傳失敗，狀態碼: {response.status_code}")
            return None

    except Exception as e:
        st.error(f"連線錯誤: {e}")
        return None
st.set_page_config(
    page_title="你觀星天文嗎？",
    page_icon="🌌",
    layout="wide"
)

# 圖片處理函數 (保持不變)
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def base64_to_image(base64_str):
    try:
        image_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_data))
    except:
        return None

# 初始化 session_state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# 🌟 簡化經緯度狀態：只保留 obs_lat 和 obs_lon
if "obs_lat" not in st.session_state:
    st.session_state.obs_lat = 25.0330 # 預設值：台北
if "obs_lon" not in st.session_state:
    st.session_state.obs_lon = 121.5654 # 預設值：台北
# st.session_state.sim_lat/sim_lon 已移除
# ==========================================
# 🏠 首頁 (保持不變)
# ==========================================
if st.session_state.current_page == "home":
    # 星星背景
    st.markdown("""
        <div class="stars">
            <div class="star" style="top: 10%; left: 20%; width: 2px; height: 2px; animation-delay: 0s;"></div>
            <div class="star" style="top: 20%; left: 80%; width: 3px; height: 3px; animation-delay: 0.5s;"></div>
            <div class="star" style="top: 30%; left: 50%; width: 2px; height: 2px; animation-delay: 1s;"></div>
            <div class="star" style="top: 50%; left: 10%; width: 3px; height: 3px; animation-delay: 1.5s;"></div>
            <div class="star" style="top: 60%; left: 70%; width: 2px; height: 2px; animation-delay: 2s;"></div>
            <div class="star" style="top: 80%; left: 30%; width: 3px; height: 3px; animation-delay: 2.5s;"></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-title"> 你觀星天文嗎？</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-subtitle">✨ 探索浩瀚星空，開啟天文之旅 ✨</div>', unsafe_allow_html=True)

    # 第一列功能 (3個)
    col1, col2, col3 = st.columns(3)

    with col1: # 🌟 天頂星座 (移動到 col1)
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌟</div>
                <div class="feature-title">天頂星座</div>
                <div class="feature-desc">點擊地圖定位，查詢天頂資訊</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("進入天頂星座", key="btn1", use_container_width=True):
            st.session_state.current_page = "天頂星座"
            st.rerun()

    with col2: # 🌌 星空模擬 (移動到 col2)
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌌</div>
                <div class="feature-title">星空模擬</div>
                <div class="feature-desc">即時互動星圖，探索天頂星座</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("進入星空模擬", key="btn_sim", use_container_width=True):
            st.session_state.current_page = "星空模擬"
            st.rerun()

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">AI 天文問答</div>
                <div class="feature-desc">使用 Gemini AI 回答天文問題</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("進入 AI 問答", key="btn2", use_container_width=True):
            st.session_state.current_page = "AI問答"
            st.rerun()

    # 第二列功能 (2個)
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">熱門話題</div>
                <div class="feature-desc">爬取天文網站，分析熱門關鍵字</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("進入熱門話題", key="btn3", use_container_width=True):
            st.session_state.current_page = "熱門話題"
            st.rerun()

    with col5:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📅</div>
                <div class="feature-title">觀星日誌</div>
                <div class="feature-desc">記錄你的每一次觀星體驗</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("進入觀星日誌", key="btn4", use_container_width=True):
            st.session_state.current_page = "觀星日誌"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #64b5f6; font-size: 1.2rem;">🔭 讓我們一起仰望星空 🌠</div>', unsafe_allow_html=True)

# 其他頁面
else:
    with st.sidebar:
        st.title("🔭 星空導覽")
        st.markdown("---")

        if st.button("🏠 返回首頁", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()

        st.markdown("---")
        options = ["🌟 天頂星座", "🌌 星空模擬", "💬 AI 天文問答", "📊 熱門話題", "📅 觀星日誌"]

        current_idx = 0
        current_label = {
            "星空模擬": "🌌 星空模擬",
            "天頂星座": "🌟 天頂星座",
            "AI問答": "💬 AI 天文問答",
            "熱門話題": "📊 熱門話題",
            "觀星日誌": "📅 觀星日誌"
        }.get(st.session_state.current_page, "🌌 星空模擬")

        if current_label in options:
            current_idx = options.index(current_label)

        page = st.radio("選擇功能", options, index=current_idx)

        page_map = {
            "🌌 星空模擬": "星空模擬",
            "🌟 天頂星座": "天頂星座",
            "💬 AI 天文問答": "AI問答",
            "📊 熱門話題": "熱門話題",
            "📅 觀星日誌": "觀星日誌"
        }

        if page_map[page] != st.session_state.current_page:
            st.session_state.current_page = page_map[page]
            st.rerun()

        st.markdown("---")
        st.info("💡 選擇左側功能開始探索星空！")



    # ==========================================
    # 🌟 頁面：天頂星座 (修正：地圖點擊只更新 obs_lat/lon)
    # ==========================================
    if st.session_state.current_page == "天頂星座":
        st.title("🌟 天頂星座查詢")
        st.markdown("### 查看您所在位置當前的天頂星座")

        col1, col2 = st.columns([2, 1])

        map_data = None

        with col1:
            st.subheader("📍 選擇觀測地點")
            st.info("💡 **點擊地圖任意位置，右側經緯度會自動更新！**")

            # 2. 建立地圖：使用 Session State 中的當前經緯度
            m = folium.Map(location=[st.session_state.obs_lat, st.session_state.obs_lon], zoom_start=8)

            # 3. 加入紅色星形標記
            folium.Marker(
                [st.session_state.obs_lat, st.session_state.obs_lon],
                popup="觀測位置",
                tooltip="目前選擇位置",
                icon=folium.Icon(color='red', icon='star')
            ).add_to(m)

            # 加入點擊顯示經緯度的功能
            m.add_child(folium.LatLngPopup())

            # 4. 顯示地圖並接收回傳數據
            map_data = st_folium(m, width=700, height=400, key="folium_map")

        # 5. 處理地圖點擊事件
        if map_data and map_data.get("last_clicked"):
            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lng = map_data["last_clicked"]["lng"]

            # 檢查是否有足夠大的變動
            if abs(clicked_lat - st.session_state.obs_lat) > 0.0001 or abs(clicked_lng - st.session_state.obs_lon) > 0.0001:
                st.session_state.obs_lat = clicked_lat # 🌟 核心：更新 obs_lat
                st.session_state.obs_lon = clicked_lng # 🌟 核心：更新 obs_lon
                # ❗ 移除 st.session_state.sim_lat/sim_lon 的操作
                st.rerun() # 重新執行腳本，地圖和輸入框將使用新的 Session State 值

        with col2:
            st.subheader("⚙️ 參數設定")

            # 🌟 修正：直接用 obs_lat 綁定
            st.number_input("緯度",
                            value=st.session_state.obs_lat,
                            format="%.4f",
                            key="obs_lat" # 綁定 Session State
                           )

            # 🌟 修正：直接用 obs_lon 綁定
            st.number_input("經度",
                            value=st.session_state.obs_lon,
                            format="%.4f",
                            key="obs_lon" # 綁定 Session State
                           )

            st.markdown("---")
            st.subheader("🕐 觀測時間")

            # 🟢 修正：先設定時區，再取得現在時刻
            taipei_tz = pytz.timezone('Asia/Taipei')
            now_taipei = datetime.now(taipei_tz)      # 這樣就會是台灣現在的時間

            # 把預設值改成 now_taipei
            obs_date = st.date_input("日期", now_taipei)
            obs_time = st.time_input("時間", now_taipei.time())


            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 查詢天頂星座", type="primary"):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
                你是一位天文專家。請根據以下資訊判斷當地此時刻的天頂星座，並用繁體中文及 Markdown 格式完整回答。

                輸入資訊：
                - 緯度：{st.session_state.obs_lat}
                - 経度：{st.session_state.obs_lon}
                - 日期：{obs_date}
                - 時間：{obs_time}

                請輸出格式如下（務必完全照此格式）：
                ### 🌌 **{{星座中文名}}（{{星座英文名}}）**
                **{{星座中文名}}（{{星座英文名}}）**是{{所屬天域}}之一

                - ⭐ 主星：{{主星名稱（英文）}}
                - 🌟 亮度：{{主星視星等}}
                - 📅 最佳觀測月份：{{月份範圍}}

                簡單介紹一下這個星座的神話故事或觀測特點 (50字以內)。
                """
                with st.spinner("天文專家計算中..."):
                    response = model.generate_content(prompt)
                    answer = response.text

                st.markdown("")
                st.markdown(answer)
    # ==========================================
    # 🌌 頁面：星空模擬 (修正：直接使用 obs_lat/lon)
    # ==========================================
    elif st.session_state.current_page == "星空模擬":
        st.title("🌌 互動式星空模擬")
        st.markdown("### 即時模擬您頭頂的星空")
        st.markdown("👇 **操作說明**：地圖是互動的！您可以拖曳旋轉星空。")

        col_ctrl1, col_ctrl2 = st.columns([1, 3])

        with col_ctrl1:
            st.subheader("⚙️ 設定")

            # 🌟 修正：直接使用 obs_lat/lon 作為 key 和 value
            # 這裡的修改會直接影響 obs_lat/lon，進而影響天頂星座頁面
            st.number_input("緯度",
                            value=st.session_state.obs_lat,
                            format="%.4f",
                            key="obs_lat" # 統一使用 obs_lat
                           )

            st.number_input("經度",
                            value=st.session_state.obs_lon,
                            format="%.4f",
                            key="obs_lon" # 統一使用 obs_lon
                           )

            st.markdown("---")
            st.markdown("**顯示選項**")
            show_constellations = st.checkbox("顯示星座連線", value=True)
            show_labels = st.checkbox("顯示星座名稱", value=True)
            show_star_labels = st.checkbox("顯示亮星名稱", value=True)
            show_grid = st.checkbox("顯示經緯網格", value=False)

            st.caption("💡 如果畫面全黑，請嘗試關閉部分選項或重新整理網頁。")

        with col_ctrl2:
            base_url = "https://virtualsky.lco.global/embed/index.html"
            params = [
                # 🌟 修正：傳遞 obs_lon/obs_lat 給 iframe
                f"longitude={st.session_state.obs_lon}",
                f"latitude={st.session_state.obs_lat}",
                "live=true",
                "projection=lambert",
                "scalestars=2",
                f"constellations={'true' if show_constellations else 'false'}",
                f"constellationlabels={'true' if show_labels else 'false'}",
                f"showstarlabels={'true' if show_star_labels else 'false'}",
                "fontscale=1.5",
                "mag=6",
                "lang=en",
                f"gridlines_az={'true' if show_grid else 'false'}",
                "mouse=true",
                "keyboard=false"
            ]
            iframe_url = f"{base_url}?{'&'.join(params)}"
            components.iframe(iframe_url, height=600, scrolling=False)
            st.caption("🔍 資料來源：Las Cumbres Observatory (VirtualSky) | 附註：為確保穩定性，星圖名稱目前僅支援英文顯示。")

    # ==========================================
    # 💬 頁面：AI 問答 (保持不變)
    # ==========================================
    elif st.session_state.current_page == "AI問答":
        st.title("💬 AI 天文知識問答")
        st.markdown("### 使用 Gemini AI 回答您的天文問題")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_question = st.chat_input("問我任何天文問題...")

        if user_question:
            with st.chat_message("user"):
                st.markdown(user_question)
            st.session_state.chat_history.append({"role": "user", "content": user_question})

            with st.chat_message("assistant"):
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("🤔 天文專家思考中...")
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"請以天文專家的角度回答以下問題：{user_question}，簡短精準的回答400字以內"
                    response = model.generate_content(prompt)
                    answer = response.text
                    thinking_placeholder.empty()
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    thinking_placeholder.empty()
                    error_msg = f"❌ API 呼叫失敗：{str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

    # ==========================================
    # 📊 頁面：熱門話題 (最終修正：使用更精確的 CSS 選擇器)
    # ==========================================
    elif st.session_state.current_page == "熱門話題":
        st.title("📊 近期天文熱門話題")

        # 初始化文章列表和文字數據，用於在 reruns 之間保持狀態
        if 'titles_data' not in st.session_state:
            st.session_state.titles_data = [] # 儲存 {title, url} 字典
        if 'all_text_data' not in st.session_state:
            st.session_state.all_text_data = ""
        if 'word_freq' not in st.session_state:
            st.session_state.word_freq = {}

        if st.button("🔄 抓取最新話題", type="primary"):
            with st.spinner("正在爬取資料..."):
                try:
                    url = "https://www.astronomy.com"
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # 🌟 修正點 1: 結構化爬蟲 (使用更精確的選擇器)
                    titles_data = []
                    base_domain = "https://www.astronomy.com"

                    # 嘗試查找兩種最可能的新聞標題連結元素：
                    # 1. 位於 h2 標籤內的 <a> 標籤
                    # 2. 位於特定 article 結構內的 <a> 標籤 (例如：.promo-item__link)

                    # 選擇器 1: 查找所有 h2 標籤下的 a 連結
                    for h2_tag in soup.find_all('h2'):
                        a_tag = h2_tag.find('a', href=True)
                        if a_tag:
                            title = a_tag.get_text(strip=True)
                            url_part = a_tag['href']

                            # 選擇器 2: 查找特定的文章列表連結 (備用或補充)
                            # 此處使用更通用的 CSS 選擇器，例如：'a[href*="/article/"]'
                            # 或者 if a_tag.parent and a_tag.parent.name == 'h2':
                            pass
                        elif h2_tag.get('class') and 'promo__title' in h2_tag.get('class'):
                            # 處理某些直接在 h2 裡的標題
                            title = h2_tag.get_text(strip=True)
                            a_tag = h2_tag.find_next('a', href=True) # 尋找 h2 後面的第一個連結
                            if a_tag:
                                url_part = a_tag['href']
                            else:
                                continue


                        # 組合完整 URL 並檢查
                        if a_tag and url_part:
                            if url_part.startswith('/'):
                                full_url = base_domain + url_part
                            elif url_part.startswith(base_domain):
                                full_url = url_part
                            else:
                                continue # 忽略外部或非文章連結

                            # 篩選標題長度和重複
                            if 10 < len(title) < 200 and full_url not in [d['url'] for d in titles_data]:
                                titles_data.append({'title': title, 'url': full_url})

                    # 額外補充：有時標題在 h3
                    for h3_tag in soup.find_all('h3'):
                        a_tag = h3_tag.find('a', href=True)
                        if a_tag:
                            title = a_tag.get_text(strip=True)
                            url_part = a_tag['href']

                            if url_part.startswith('/'):
                                full_url = base_domain + url_part
                            elif url_part.startswith(base_domain):
                                full_url = url_part
                            else:
                                continue

                            if 10 < len(title) < 200 and full_url not in [d['url'] for d in titles_data]:
                                titles_data.append({'title': title, 'url': full_url})


                    # 將結果存入 Session State
                    st.session_state.titles_data = titles_data
                    titles = [d['title'] for d in titles_data] # 用於文字雲分析

                    # 🌟 修正點 2: 文字雲處理 (保持原樣，但使用 titles 列表)
                    stopwords_en = ['the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'were', 'have', 'has', 'new', 'time', 'will', 'say', 'can', 'find', 'get', 'out', 'into', 'is'] # 增加一些常見停用詞
                    stopwords_zh = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一個', '上', '也', '很', '到', '說', '要', '去', '你', '會', '著', '沒有', '看', '好', '自己', '這']

                    all_text = ' '.join(titles)
                    st.session_state.all_text_data = all_text # 存入 Session State

                    words_en = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', all_text) if w.lower() not in stopwords_en and len(w) > 3]
                    chinese_text = re.sub(r'[a-zA-Z0-9\s]+', '', all_text)
                    words_zh = [w for w in jieba.cut(chinese_text) if w not in stopwords_zh and len(w) > 1 and w.strip()]
                    all_words = words_en + words_zh
                    word_freq = Counter(all_words)
                    st.session_state.word_freq = word_freq # 存入 Session State

                    st.success(f"✅ 資料抓取完成！共找到 {len(titles_data)} 篇文章。")

                except Exception as e:
                    st.error(f"❌ 爬取失敗：{str(e)}，請檢查網路連線或目標網站結構是否改變。")
                    st.session_state.titles_data = [] # 失敗時清空數據
                    st.session_state.word_freq = {}


        # 顯示爬取結果 (無論是否重新爬取，只要 Session State 有數據就顯示)
        if st.session_state.titles_data:
            col1, col2 = st.columns([2, 1])

            # 顯示文字雲
            with col1:
                st.subheader("☁️ 熱門關鍵字文字雲")
                if st.session_state.word_freq:
                    # 確保 simsun.ttc 存在或使用 Streamlit 支援的其他中文字型路徑
                    try:
                        wordcloud = WordCloud(width=800, height=400, background_color='#0a0e27', colormap='Blues', font_path='simsun.ttc').generate_from_frequencies(st.session_state.word_freq)
                    except:
                        # 如果 simsun.ttc 不可用，使用預設字型
                        wordcloud = WordCloud(width=800, height=400, background_color='#0a0e27', colormap='Blues').generate_from_frequencies(st.session_state.word_freq)

                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                else:
                    st.warning("未找到足夠的關鍵字")

            # 顯示 Top 10 關鍵字
            with col2:
                st.subheader("🔥 Top 10 熱門關鍵字")
                if st.session_state.word_freq:
                    df = pd.DataFrame(st.session_state.word_freq.most_common(10), columns=['關鍵字', '次數'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("暫無數據")

            # 🌟 修正點 3: 顯示文章列表與網址
            st.subheader("📰 最新文章及連結 (Top 10)")

            # 使用一個容器來調整列表的整體字體大小
            st.markdown(
                """
                <style>
                /* 針對整個列表區塊的文字，設定比預設更大的字體 */
                .article-list-item {
                    font-size: 1.1em; /* 略微放大字體 */
                    line-height: 2.0; /* 增加行距，讓閱讀更舒適 */
                }
                /* 確保連結本身是藍色的 */
                .article-list-item a {
                    color: #0080ff !important; /* 藍色 */
                    text-decoration: none; /* 移除預設底線 */
                }
                .article-list-item a:hover {
                    text-decoration: underline; /* 滑鼠移上去時出現底線 */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            if st.session_state.titles_data:
                for i, item in enumerate(st.session_state.titles_data[:10], 1):
                    # 建立結構：[編號]. [白色標題] ([藍色連結])
                    html_link = f"""
                    <div class="article-list-item">
                        {i}.
                        <span style="color: white; font-weight: bold;">
                            {item['title']}
                        </span>
                        <span style="color: #cccccc;"> (</span>
                        <a href="{item['url']}" target="_blank">
                            {item['url']}
                        </a>
                        <span style="color: #cccccc;">)</span>
                    </div>
                    """
                    st.markdown(html_link, unsafe_allow_html=True)
            else:
                st.info("未抓取到有效的文章連結。")

        # 確保這個 elif 在 if st.session_state.titles_data: 區塊之外
        elif not st.session_state.titles_data:
            st.info("點擊上方的按鈕抓取 `Astronomy.com` 的最新天文話題！")

    # ==========================================
    # 📅 頁面：觀星日誌 (整合刪除功能)
    # ==========================================
    if st.session_state.get("current_page") == "觀星日誌":  # 如果是在多頁面結構中，請改回 elif
        st.title("📅 我的觀星日誌")

        # 加入 CSS 來縮小行距與 Padding，讓列表更緊湊，並修飾按鈕
        st.markdown("""
            <style>
                /* 縮小區塊間的垂直間距 */
                .block-container { padding-top: 1rem; }
                div[data-testid="column"] { padding: 0px; }
                /* 調整分隔線樣式 */
                hr { margin: 0.5em 0; border-color: #eee; }
                /* 讓文字行高緊湊一點 */
                p { margin-bottom: 0.2rem; }
                /* 針對刪除按鈕做一點微調，確保對齊 */
                div[data-testid="stButton"] button {
                    border-color: #ffcccc;
                    color: #d9534f;
                }
                div[data-testid="stButton"] button:hover {
                    border-color: #d9534f;
                    color: white;
                    background-color: #d9534f;
                }
            </style>
        """, unsafe_allow_html=True)

        # 嘗試連線
        try:
            worksheet = connect_to_gsheet()
        except NameError:
            st.error("❌ 找不到 connect_to_gsheet 函式，請確認是否已定義。")
            worksheet = None

        if worksheet:
            # 初始化 Sheet (假設函式存在)
            try:
                init_sheet(worksheet)
            except:
                pass # 忽略初始化錯誤，避免卡住

            # 載入日誌到 Session State
            if 'logs_loaded' not in st.session_state:
                st.session_state.logs = load_logs_from_sheet(worksheet)
                st.session_state.logs_loaded = True

            # 初始化刪除狀態
            if 'confirm_delete' not in st.session_state:
                st.session_state['confirm_delete'] = None

            # --- 1. 新增觀星記錄區塊 ---
            with st.expander("➕ 新增觀星記錄", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    log_date = st.date_input("📅 觀測日期", datetime.now())
                    log_location = st.text_input("📍 觀測地點", "台北")
                    log_weather = st.select_slider("🌤️ 天氣", options=["多雲", "晴朗", "極佳"])
                with col2:
                    log_constellation = st.text_input("🌟 觀測星座", "獵戶座")
                    log_equipment = st.text_input("🔭 器材", "雙筒望遠鏡")
                    log_rating = st.slider("⭐ 評分", 1, 5, 4)

                log_notes = st.text_area("📝 筆記", placeholder="記錄觀測心得...")
                st.markdown("### 📷 上傳觀星照片")
                uploaded_file = st.file_uploader("選擇照片", type=['png', 'jpg', 'jpeg'], key="photo_uploader")

                # 預覽邏輯
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    image.thumbnail((800, 800))
                    col_preview1, col_preview2, col_preview3 = st.columns([1, 2, 1])
                    with col_preview2:
                        st.image(image, caption="📷 照片預覽", use_container_width=True)

                if st.button("💾 儲存記錄", type="primary"):
                    photo_url = "" # 初始化為空字串

                    # 如果有上傳照片，先執行上傳
                    if uploaded_file is not None:
                        with st.spinner("☁️ 正在上傳照片到雲端 (Catbox)..."):
                            # 需確認 upload_to_catbox 函式存在
                            photo_url = upload_to_catbox(uploaded_file)

                            if not photo_url:
                                st.error("❌ 照片上傳失敗，請重試或檢查網路。")
                                st.stop() # 停止執行，避免存入沒有照片的紀錄

                    # 準備要寫入 Google Sheet 的資料
                    new_log = {
                        "date": log_date.strftime("%Y-%m-%d"),
                        "location": log_location,
                        "weather": log_weather,
                        "constellation": log_constellation,
                        "equipment": log_equipment,
                        "rating": log_rating,
                        "notes": log_notes,
                        "photo": photo_url  # 這裡存的是網址
                    }

                    # 寫入 Sheet
                    if save_log_to_sheet(worksheet, new_log):
                        st.session_state.logs.append(new_log)
                        st.success("✅ 記錄已儲存！")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ 儲存失敗，請檢查 Google Sheets 設定")

            # --- 2. 刪除確認視窗 (優先顯示) ---
            if st.session_state.confirm_delete is not None:
                # 取得要刪除的資料
                row_to_delete = st.session_state.confirm_delete
                log_index_to_delete = st.session_state.delete_log_index
                log_data = st.session_state.log_to_delete

                st.warning(f"⚠️ **確定要刪除這筆記錄嗎？**")
                st.markdown(f"> 📅 **{log_data['date']}** | 📍 **{log_data['location']}** | 🌟 **{log_data['constellation']}**")

                col_confirm1, col_confirm2, col_confirm3 = st.columns([1, 1, 3])
                with col_confirm1:
                    if st.button("✅ 確認刪除", type="primary"):
                        # 1. 刪除 Google Sheet 上的資料
                        if delete_log_from_sheet(worksheet, row_to_delete):
                            # 2. 刪除 Streamlit session state 中的資料
                            del st.session_state.logs[log_index_to_delete]
                            st.success("🗑️ 記錄已成功刪除！")

                            # 3. 清除確認狀態並重新運行
                            st.session_state.confirm_delete = None
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ 刪除失敗，請檢查 Google Sheets 設定或權限。")
                with col_confirm2:
                    if st.button("❌ 取消"):
                        st.session_state.confirm_delete = None
                        st.rerun()

                # 如果有確認視窗，停止執行後續程式碼（不顯示列表）
                st.stop()

            # --- 3. 顯示觀星記錄區塊 (緊湊條列版 + 整合刪除鈕) ---
            if st.session_state.logs:
                st.subheader("📖 觀星記錄")

                # 重新載入按鈕
                if st.button("🔄 重新載入"):
                    st.session_state.logs = load_logs_from_sheet(worksheet)
                    st.rerun()

                st.markdown("---") # 標題下方的大分隔線

                # 開始迴圈
                for i, log in enumerate(reversed(st.session_state.logs)):

                    # 計算索引
                    log_index = len(st.session_state.logs) - 1 - i
                    sheet_row_index = log_index + 2

                    # 使用 container 包住每一行
                    with st.container():
                        # 定義四個欄位：
                        # 修改比例：稍微縮小筆記欄(4->3.5)，加大動作欄(1->1.2) 以容納「刪除」文字
                        c_img, c_info, c_note, c_action = st.columns([1.5, 2, 3.5, 1.2], gap="small")

                        # --- Col 1: 小縮圖 ---
                        with c_img:
                            if log.get('photo') and log['photo'].startswith("http"):
                                st.image(log['photo'], width=120)
                            elif log.get('photo') and len(log['photo']) > 100:
                                try:
                                    img = base64_to_image(log['photo'])
                                    st.image(img, width=120)
                                except:
                                    st.text("無圖")
                            else:
                                st.markdown("## 🔭")

                        # --- Col 2: 核心資訊 ---
                        with c_info:
                            st.markdown(f"**📅 {log['date']}**")
                            st.caption(f"📍 {log['location']}")
                            st.text(f"🌟 {log['constellation']}")
                            st.text(f"⭐ {'★' * int(log['rating'])}")

                        # --- Col 3: 筆記與天氣 ---
                        with c_note:
                            st.markdown(f"**🌤️ {log['weather']}** | 🔭 {log['equipment']}")

                            note_text = log['notes']
                            if len(note_text) > 40: # 稍微減少預覽字數，配合縮小的欄寬
                                note_preview = note_text[:40] + "..."
                            else:
                                note_preview = note_text or "(無筆記)"

                            st.markdown(f"<span style='color:gray; font-size:0.9em;'>📝 {note_preview}</span>", unsafe_allow_html=True)

                            with st.expander("詳細"):
                                st.write(note_text)
                                if log.get('photo') and log['photo'].startswith("http"):
                                    st.image(log['photo'], use_container_width=True)

                        # --- Col 4: 整合後的刪除按鈕 ---
                        with c_action:
                            # 垂直置中用
                            st.write("")
                            # 這裡改成第二版的按鈕樣式：有文字、secondary 樣式
                            if st.button("🗑️ 刪除", key=f"del_{i}", type="secondary"):
                                st.session_state['confirm_delete'] = sheet_row_index
                                st.session_state['delete_log_index'] = log_index
                                st.session_state['log_to_delete'] = log
                                st.rerun()

                    # --- 自訂分隔線 ---
                    st.markdown("<hr style='margin: 8px 0; border-color: #f0f0f0;'>", unsafe_allow_html=True)

            elif st.session_state.logs_loaded:
                st.info("目前沒有觀星記錄，快新增第一筆吧！")

        else:
            st.error("❌ 無法連線到 Google Sheets，請檢查設定。")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #64b5f6;"><p>🌌 你觀星天文嗎？| Made with Streamlit ✨</p></div>', unsafe_allow_html=True)
