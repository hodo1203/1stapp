import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="삼각함수 학습 웹앱", layout="wide")

st.title("📐 삼각함수 인터랙티브 학습 웹앱")
st.markdown("수학과제탐구 수행평가를 위한 삼각함수 학습 도구입니다. 모든 각도와 값은 **라디안(radian)**을 기준으로 표시됩니다.")

# 사이드바 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴 선택",
    [
        "1. 삼각함수 그래프 & 역함수 탐구",
        "2. 단위 원과 삼각함수 연동 시각화",
        "3. 특수각 삼각함수 값 표",
        "4. 삼각함수 각변환 퀴즈"
    ]
)

# ---------------------------------------------------------
# 메뉴 1: 삼각함수 그래프 & 역함수 탐구
# ---------------------------------------------------------
if menu == "1. 삼각함수 그래프 & 역함수 탐구":
    st.header("1. 삼각함수 그래프 시각적으로 확인하기")
    st.markdown("상단에서 함수의 종류, 진폭, 주기, 평행이동 등을 조절하고, 하단에서 특정 $y$값에 해당하는 $x$값을 확인해보세요.")
    
    st.sidebar.subheader("🎛️ 그래프 설정 요인")
    func_type = st.sidebar.selectbox("함수 선택", ["사인 (Sine)", "코사인 (Cosine)", "탄젠트 (Tangent)"])
    amplitude = st.sidebar.slider("진폭 (최댓값 조절)", 0.5, 5.0, 1.0, 0.5)
    period_mult = st.sidebar.slider("주기 조절 배율", 0.5, 3.0, 1.0, 0.25)
    phase_shift = st.sidebar.slider("위상(평행이동) [라디안]", -np.pi, np.pi, 0.0, 0.1)
    vertical_shift = st.sidebar.slider("수직이동", -3.0, 3.0, 0.0, 0.5)

    # x 범위 설정 및 데이터프레임 생성 (Streamlit 내장 차트 활용)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    
    if "사인" in func_type:
        y = amplitude * np.sin(period_mult * x - phase_shift) + vertical_shift
        chart_data = pd.DataFrame({"x": x, "y (Sine)": y})
    elif "코사인" in func_type:
        y = amplitude * np.cos(period_mult * x - phase_shift) + vertical_shift
        chart_data = pd.DataFrame({"x": x, "y (Cosine)": y})
    else:
        y = amplitude * np.tan(period_mult * x - phase_shift) + vertical_shift
        y[np.abs(np.gradient(y)) > 30] = np.nan  # 점근선 처리
        chart_data = pd.DataFrame({"x": x, "y (Tangent)": y})

    chart_data.set_index("x", inplace=True)
    st.line_chart(chart_data)
    
    # 역함수 (y값에 따른 x값 찾기) 기능
    st.subheader("🔍 특정 y값에 따른 x 찾기 (역함수 탐색)")
    col1, col2 = st.columns(2)
    with col1:
        target_y = st.number_input("찾을 y값 입력", value=0.0, step=0.1)
    with col2:
        x_min_range = st.number_input("x 범위 최소값 (라디안)", value=float(-2*np.pi), step=0.5)
        x_max_range = st.number_input("x 범위 최대값 (라디안)", value=float(2*np.pi), step=0.5)

    x_fine = np.linspace(x_min_range, x_max_range, 2000)
    if "사인" in func_type:
        y_fine = amplitude * np.sin(period_mult * x_fine - phase_shift) + vertical_shift
    elif "코사인" in func_type:
        y_fine = amplitude * np.cos(period_mult * x_fine - phase_shift) + vertical_shift
    else:
        y_fine = amplitude * np.tan(period_mult * x_fine - phase_shift) + vertical_shift

    diff = y_fine - target_y
    sign_changes = np.where(np.diff(np.signbit(diff)))[0]
    found_x = []
    for idx in sign_changes:
        x1, x2 = x_fine[idx], x_fine[idx+1]
        y1, y2 = diff[idx], diff[idx+1]
        if y2 - y1 != 0:
            x_root = x1 - y1 * (x2 - x1) / (y2 - y1)
            found_x.append(x_root)

    if found_x:
        st.success(f"입력하신 y = {target_y} 에 해당하는 x값 (지정 범위 내): " + ", ".join([f"{fx:.3f} 라디안" for fx in found_x]))
    else:
        st.info("지정한 범위 내에서 해당 y값을 갖는 x가 존재하지 않습니다.")


# ---------------------------------------------------------
# 메뉴 2: 단위 원과 삼각함수 연동 시각화
# ---------------------------------------------------------
elif menu == "2. 단위 원과 삼각함수 연동 시각화":
    st.header("2. 원을 통한 삼각함수 시각적으로 파악하기")
    st.markdown("슬라이더를 통해 각도(라디안)를 조절하고 삼각함숫값의 변화를 확인해보세요.")

    theta = st.slider("각도 설정 (라디안)", 0.0, float(2 * np.pi), float(np.pi / 4), 0.05)
    
    cos_val = np.cos(theta)
    sin_val = np.sin(theta)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 각도", f"{theta:.2f} 라디안", f"{np.degrees(theta):.1f}°")
    col2.metric("코사인 값 (cos)", f"{cos_val:.4f}")
    col3.metric("사인 값 (sin)", f"{sin_val:.4f}")
    if np.cos(theta) != 0:
        col3.metric("탄젠트 값 (tan)", f"{np.tan(theta):.4f}")
    else:
        col3.metric("탄젠트 값 (tan)", "정의되지 않음 (무한대)")

    st.markdown("---")
    show_sin = st.checkbox("사인함수 (sin x) 값 보기", value=True)
    show_cos = st.checkbox("코사인함수 (cos x) 값 보기", value=True)
    show_tan = st.checkbox("탄젠트함수 (tan x) 값 보기", value=False)

    x_vals = np.linspace(0, 2 * np.pi, 200)
    plot_dict = {}
    if show_sin:
        plot_dict["sin(x)"] = np.sin(x_vals)
    if show_cos:
        plot_dict["cos(x)"] = np.cos(x_vals)
    if show_tan:
        t_vals = np.tan(x_vals)
        t_vals[np.abs(np.gradient(t_vals)) > 20] = np.nan
        plot_dict["tan(x)"] = t_vals

    df_plot = pd.DataFrame(plot_dict, index=x_vals)
    st.line_chart(df_plot)


# ---------------------------------------------------------
# 메뉴 3: 특수각 삼각함수 값 표
# ---------------------------------------------------------
elif menu == "3. 특수각 삼각함수 값 표":
    st.header("3. 사인, 코사인, 탄젠트 특수각 값 표")
    st.markdown("0도부터 90도까지의 특수각 값을 라디안 표기로 정리하여 제공합니다.")

    data = {
        "각도 (도)": ["0°", "30°", "45°", "60°", "90°"],
        "각도 (라디안)": ["0", "$\\frac{\\pi}{6}$", "$\\frac{\\pi}{4}$", "$\\frac{\\pi}{3}$", "$\\frac{\\pi}{2}$"],
        "사인 (sin)": ["0", "$\\frac{1}{2}$", "$\\frac{\\sqrt{2}}{2}$", "$\\frac{\\sqrt{3}}{2}$", "1"],
        "코사인 (cos)": ["1", "$\\frac{\\sqrt{3}}{2}$", "$\\frac{\\sqrt{2}}{2}$", "$\\frac{1}{2}$", "0"],
        "탄젠트 (tan)": ["0", "$\\frac{\\sqrt{3}}{3}$", "1", "$\\sqrt{3}$", "존재하지 않음"]
    }

    df = pd.DataFrame(data)
    st.table(df)


# ---------------------------------------------------------
# 메뉴 4: 삼각함수 각변환 퀴즈
# ---------------------------------------------------------
elif menu == "4. 삼각함수 각변환 퀴즈":
    st.header("4. 삼각함수 각변환 퀴즈 (총 10문제)")
    st.markdown("각변환 공식을 학습하기 위한 퀴즈입니다. 틀리면 한 번 더 기회가 제공됩니다.")

    quiz_questions = [
        {"id": 1, "q": "$\\sin\\left(\\frac{\\pi}{2} - \\theta\\right)$ 와 같은 것은?", "options": ["$\\sin\\theta$", "$-\\sin\\theta$", "$\\cos\\theta$", "$-\\cos\\theta$"], "answer": "$\\cos\\theta$", "explanation": "여각 공식에 의해 $\\sin(\\frac{\\pi}{2} - \\theta) = \\cos\\theta$ 입니다."},
        {"id": 2, "q": "$\\cos(\\pi + \\theta)$ 와 같은 것은?", "options": ["$\\cos\\theta$", "$-\\cos\\theta$", "$\\sin\\theta$", "$-\\sin\\theta$"], "answer": "$-\\cos\\theta$", "explanation": "제3사분면에서 코사인의 부호는 음수이므로 $\\cos(\\pi + \\theta) = -\\cos\\theta$ 입니다."},
        {"id": 3, "q": "$\\tan\\left(\\frac{\\pi}{2} + \\theta\\right)$ 와 같은 것은?", "options": ["$\\tan\\theta$", "$-\\tan\\theta$", "$\\frac{1}{\\tan\\theta}$", "$-\\frac{1}{\\tan\\theta}$"], "answer": "$-\\frac{1}{\\tan\\theta}$", "explanation": "제2사분면에서 탄젠트가 음수이고 역수가 되므로 $-\\frac{1}{\\tan\\theta}$ 입니다."},
        {"id": 4, "q": "$\\sin(\\pi - \\theta)$ 와 같은 것은?", "options": ["$\\sin\\theta$", "$-\\sin\\theta$", "$\\cos\\theta$", "$-\\cos\\theta$"], "answer": "$\\sin\\theta$", "explanation": "제2사분면에서 사인의 부호는 양수이므로 $\\sin(\\pi - \\theta) = \\sin\\theta$ 입니다."},
        {"id": 5, "q": "$\\cos(2\\pi - \\theta)$ 와 같은 것은?", "options": ["$\\cos\\theta$", "$-\\cos\\theta$", "$\\sin\\theta$", "$-\\sin\\theta$"], "answer": "$\\cos\\theta$", "explanation": "제4사분면에서 코사인의 부호는 양수이므로 $\\cos(2\\pi - \\theta) = \\cos\\theta$ 입니다."},
        {"id": 6, "q": "$\\sin\\left(\\frac{\\pi}{2} + \\theta\\right)$ 와 같은 것은?", "options": ["$\\sin\\theta$", "$-\\sin\\theta$", "$\\cos\\theta$", "$-\\cos\\theta$"], "answer": "$\\cos\\theta$", "explanation": "제2사분면에서 사인의 부호는 양수이고 함수명이 바뀌어 $\\cos\\theta$가 됩니다."},
        {"id": 7, "q": "$\\tan(\\pi - \\theta)$ 와 같은 것은?", "options": ["$\\tan\\theta$", "$-\\tan\\theta$", "$-\\frac{1}{\\tan\\theta}$", "$\\frac{1}{\\tan\\theta}$"], "answer": "$-\\tan\\theta$", "explanation": "제2사분면에서 탄젠트의 부호는 음수이므로 $\\tan(\\pi - \\theta) = -\\tan\\theta$ 입니다."},
        {"id": 8, "q": "$\\cos\\left(\\frac{\\pi}{2} + \\theta\\right)$ 와 같은 것은?", "options": ["$\\sin\\theta$", "$-\\sin\\theta$", "$\\cos\\theta$", "$-\\cos\\theta$"], "answer": "$-\\sin\\theta$", "explanation": "제2사분면에서 코사인의 부호는 음수이고 함수명이 바뀌어 $-\\sin\\theta$가 됩니다."},
        {"id": 9, "q": "$\\sin(-\\theta)$ 와 같은 것은?", "options": ["$\\sin\\theta$", "$-\\sin\\theta$", "$\\cos\\theta$", "$-\\cos\\theta$"], "answer": "$-\\sin\\theta$", "explanation": "사인은 원점을 지나는 기함수이므로 $\\sin(-\\theta) = -\\sin\\theta$ 입니다."},
        {"id": 10, "q": "$\\cos(-\\theta)$ 와 같은 것은?", "options": ["$\\cos\\theta$", "$-\\cos\\theta$", "$\\sin\\theta$", "$-\\sin\\theta$"], "answer": "$\\cos\\theta$", "explanation": "코사인은 y축 대칭인 우함수이므로 $\\cos(-\\theta) = \\cos\\theta$ 입니다."}
    ]

    if "quiz_states" not in st.session_state:
        st.session_state.quiz_states = {
            q["id"]: {"attempts": 0, "solved": False, "failed": False} for q in quiz_questions
        }

    correct_count = sum(1 for qid, st_val in st.session_state.quiz_states.items() if st_val["solved"])
    st.progress(correct_count / len(quiz_questions))
    st.write(f"현재 맞힌 문제: **{correct_count} / {len(quiz_questions)}**")

    for idx, item in enumerate(quiz_questions):
        qid = item["id"]
        q_state = st.session_state.quiz_states[qid]

        with st.expander(f"문제 {qid}. {item['q']}", expanded=not q_state["solved"]):
            if q_state["solved"]:
                st.success("✅ 정답입니다!")
                st.write(f"**해설:** {item['explanation']}")
            elif q_state["failed"]:
                st.error("❌ 오답입니다. 해설을 참고하여 다시 풀어보세요!")
                st.info(f"**해설:** {item['explanation']}")
                
                user_choice_retry = st.radio(f"재도전 (문제 {qid})", item["options"], key=f"retry_{qid}")
                if st.button("다시 제출", key=f"btn_retry_{qid}"):
                    if user_choice_retry == item["answer"]:
                        st.session_state.quiz_states[qid]["solved"] = True
                        st.session_state.quiz_states[qid]["failed"] = False
                        st.rerun()
                    else:
                        st.warning("아직 정답이 아닙니다.")
            else:
                user_choice = st.radio(f"정답을 선택하세요:", item["options"], key=f"choice_{qid}")
                if st.button("정답 제출", key=f"btn_{qid}"):
                    if user_choice == item["answer"]:
                        st.session_state.quiz_states[qid]["solved"] = True
                        st.rerun()
                    else:
                        st.session_state.quiz_states[qid]["attempts"] += 1
                        st.session_state.quiz_states[qid]["failed"] = True
                        st.rerun()

    if correct_count == len(quiz_questions):
        st.balloons()
        st.success("🎉 축하합니다! 모든 퀴즈를 완료했습니다!")
