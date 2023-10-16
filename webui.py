import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address


api = ApiRequest(base_url=api_address())
def get_user_info(token):
    user_info = api.get_user_info(token)
    return user_info

if __name__ == "__main__":

    # 查询 URL 中的参数
    params = st.experimental_get_query_params()
    print(params)

    # 发送 GET请求 http://82.156.16.203/api/getInfo
    print("get user info")
    user_info =  get_user_info(params["token"][0]) if "token" in params else {}

    # 判断 params 中是否有 token 参数
    st.set_page_config(
        "AI Chat",
        os.path.join("img", "logo.png"),
        initial_sidebar_state="expanded",
        menu_items={
            # 'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat',
            # 'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            # 'About': f"""欢迎使用 Langchain-Chatchat WebUI {VERSION}！"""
        }
    )

    # if not chat_box.chat_inited:
    #     st.toast(
    #         f"欢迎使用 [`Langchain-Chatchat`](https://github.com/chatchat-space/Langchain-Chatchat) ! \n\n"
    #         f"当前使用模型`{LLM_MODEL}`, 您可以开始提问了."
    #     )

    pages = {
        "对话": {
            "icon": "chat",
            "func": dialogue_page,
        }
    }

    # 如果是登录用户，显示知识库管理页面
    if "roles" in user_info and "admin" in user_info["roles"]:
        pages["知识库管理"] = {
            "icon": "hdd-stack",
            "func": knowledge_base_page,
        }

    with st.sidebar:
        # st.image(
        #     os.path.join(
        #         "img",
        #         "logo.png"
        #     ),
        #     width=80,
        #
        #     # use_column_width=True,
        #
        # )
        # st.caption(
        #     f"""<p align="right">当前版本：{VERSION}</p>""",
        #     unsafe_allow_html=True,
        # )
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )

    if selected_page in pages:
        pages[selected_page]["func"](api)
