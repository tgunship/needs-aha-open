# Copyright © 2026 Takeshi Uchida

import streamlit as st
import random

# --- アプリ全体の背景色と基本デザインの設定 ---
st.markdown("""
    <style>
    /* 画面全体の背景色を柔らかなアイボリーに */
    .stApp {
        background-color: #FDFBF7;
    }
    /* チェックボックスのテキストを少し大きく */
    .stCheckbox label span {
        font-size: 18px !important;
        color: #4A4A4A;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. ニーズリスト ---
DEFAULT_NEEDS = [
    "共感", "受容", "理解", "尊重", "思いやり", 
    "信頼", "所属", "愛", "感謝", "親密さ", 
    "つながり", "支え・協力", "相互性", "循環", "豊かさ",
    "自由・選択", "自律", "空間・間", "自発性", "自分に本物であること", 
    "言行一致・誠実さ", "自己表現", "意味・目的", "貢献", "成長", 
    "探求・発見", "創造性", "内なる力", "効力感・達成", "明確さ",
    "嘆き・悼み", "インスピレーション・直感", "平和・調和", "ただ在ること", "流れ・フロー", 
    "秩序", "平等・公平", "美", "身体の安全", "安心", 
    "休息", "心身の滋養", "ふれあい", "活力・いのちの躍動", "希望", 
    "安らげる居場所", "遊び・気軽さ", "喜び", "祝福", "挑戦・刺激"
]

st.title("🎯 ニーズ アハ！")
# タイトルの直下に小さくバージョン情報を表示
st.markdown("<div style='font-size: 14px; color: #888888; margin-top: -15px; margin-bottom: 20px;'>カードオープン版 Ver1.00</div>", unsafe_allow_html=True)

# --- 2. 初期設定 ---
if 'candidates' not in st.session_state:
    st.session_state.candidates = DEFAULT_NEEDS.copy()
    random.shuffle(st.session_state.candidates) # 最初だけランダムに並び替え
    st.session_state.round_count = 1
    st.session_state.finished = False

# 候補が1つだけになったら終了判定
if len(st.session_state.candidates) == 1:
    st.session_state.finished = True

# --- 3. 画面表示（結果発表 または 選択画面） ---
if st.session_state.finished:
    # === 結果画面 ===
    st.balloons() # お祝いのエフェクト
    
    final_need = st.session_state.candidates[0]
    
    # メッセージ
    st.markdown("<h2 style='text-align: center; color: #D35400;'>アハ！ 見つかりましたね！</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666666;'>今のあなたの心のど真ん中にある、一番大切にしたいニーズは...</p>", unsafe_allow_html=True)
    
    # 結果を強調する特別なカードデザイン
    st.markdown(
        f"""
        <div style="
            padding: 50px 20px; 
            background: linear-gradient(135deg, #FFF0D1 0%, #FFDCA8 100%); 
            border: 2px solid #FFC266;
            border-radius: 20px; 
            text-align: center; 
            box-shadow: 0 8px 15px rgba(211, 84, 0, 0.15);
            margin: 30px 0;">
            <h1 style="color: #C0392B; margin:0; font-size: 48px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">
                {final_need}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("もう一度、心に問いかける", use_container_width=True):
        # セッション状態をクリアしてリセット
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

else:
    # === 選択画面 ===
    st.markdown(f"**ラウンド {st.session_state.round_count}**： 現在 **{len(st.session_state.candidates)}** 個の候補があります。")
    
    # ユーザーに「最終的に1つに絞る」というゴールを伝える案内文
    st.info(
        "💡 **最終的に「これだ！」という1つのニーズに絞り込んでいきます。**\n\n"
        "今のリストから、直感でピンときたものを**いくつでも**チェックして、「しぼりこみ！」を押してください。"
    )
    
    # フォームを使用して、ボタンが押されるまで画面を更新しないようにする
    with st.form("selection_form"):
        # 3列のグリッド表示にする
        cols = st.columns(3)
        selected_needs = []
        
        # 候補リストをチェックボックスとして表示
        for i, need in enumerate(st.session_state.candidates):
            with cols[i % 3]: # 0,1,2 の列に順番に配置
                # keyにラウンド数を入れることで、ラウンドが変わるごとにチェックをリセットする
                if st.checkbox(need, key=f"chk_{need}_{st.session_state.round_count}"):
                    selected_needs.append(need)
        
        st.write("") # 少し余白を空ける
        
        # 送信ボタン
        submitted = st.form_submit_button("しぼりこみ！", type="primary", use_container_width=True)
        
        # ボタンが押されたあとの処理
        if submitted:
            if len(selected_needs) == 0:
                # 1つも選ばれなかった場合の警告（画面は進まない）
                st.error("⚠️ 最低でも1つはチェックしてください！")
            else:
                # 選ばれたものだけを次の候補リストに上書き
                st.session_state.candidates = selected_needs
                st.session_state.round_count += 1
                st.rerun() # 画面を更新して次のラウンドへ

# --- 4. コピーライト表示（フッター） ---
st.markdown(
    """
    <div style="text-align: center; padding-top: 50px; color: #999999; font-size: 14px;">
        Copyright &copy; 2026 Takeshi Uchida
    </div>
    """, 
    unsafe_allow_html=True
)
