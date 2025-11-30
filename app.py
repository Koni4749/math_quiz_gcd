import streamlit as st
import random
import math
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="중1 소인수분해 퀴즈", page_icon="🎓", layout="wide")

# 스타일
st.markdown("""
<style>
.big-title { font-size:35px; font-weight:700; text-align:center; }
.sub-card { 
    padding:20px; 
    background:#f7f7f9; 
    border-radius:10px;  
    border:1px solid #ddd; 
    margin-bottom: 20px;
}
.result-card {
    padding:25px; 
    background:#eef9ff; 
    border-radius:10px;  
    border:2px solid #40a6ff; 
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

#-------------------------------------------------
# 기존 함수들
#-------------------------------------------------
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def get_divisor_count(n):
    count = 1
    d = 2
    temp = n
    while d*d <= temp:
        if temp % d == 0:
            exponent = 0
            while temp % d == 0:
                exponent += 1
                temp //= d
            count *= (exponent + 1)
        d += 1
    if temp > 1:
        count *= 2
    return count

def check_factorization(user_str, target_num):
    clean_str = user_str.replace(" ", "").lower().replace("x", "*")
    if not clean_str:
        return False
    allowed = set("0123456789*^")
    if not set(clean_str).issubset(allowed):
        return False

    terms = clean_str.split('*')
    calculated_value = 1

    for term in terms:
        if term == "":
            continue
        if '^' in term:
            parts = term.split('^')
            if len(parts) != 2:
                return False
            base_str, exp_str = parts[0], parts[1]
            if not base_str.isdigit() or not exp_str.isdigit():
                return False
            base, exp = int(base_str), int(exp_str)
        else:
            if not term.isdigit():
                return False
            base, exp = int(term), 1

        if not is_prime(base):
            return False

        calculated_value *= (base ** exp)

    return calculated_value == target_num

def get_needed_number_for_square(n):
    result = 1
    d = 2
    temp = n
    while d*d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            if count % 2 != 0:
                result *= d
        d += 1
    if temp > 1:
        result *= temp
    return result

#-------------------------------------------------
# 세션 상태 초기화
#-------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.answers = {}  # 사용자가 입력한 답
    st.session_state.data = {}
    st.session_state.record = []

#-------------------------------------------------
# 문제 데이터 생성
#-------------------------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True

    # 문제 1
    num1 = random.randint(12, 100)
    while is_prime(num1):
        num1 = random.randint(12, 100)
    st.session_state.data["num1"] = num1

    # 문제 2
    c1, c2 = random.randint(10, 30), random.randint(10, 30)
    while c1 == c2:
        c2 = random.randint(10, 30)
    st.session_state.data["c1"] = c1
    st.session_state.data["c2"] = c2

    # 문제 3
    while True:
        g1, g2 = random.randint(12, 60), random.randint(12, 60)
        if math.gcd(g1, g2) > 1:
            break
    st.session_state.data["g1"] = g1
    st.session_state.data["g2"] = g2

    # 문제 4
    cd1, cd2 = random.randint(20, 100), random.randint(20, 100)
    st.session_state.data["cd1"] = cd1
    st.session_state.data["cd2"] = cd2

    # 문제 5
    st.session_state.data["l1"] = random.randint(4, 30)
    st.session_state.data["l2"] = random.randint(4, 30)

    # 문제 6
    st.session_state.data["bus_a"] = random.randint(4, 9)
    st.session_state.data["bus_b"] = random.randint(10, 15)

    # 문제 7
    while True:
        a = random.randint(6, 20)
        b = random.randint(6, 20)
        if math.gcd(a, b) > 1:
            break
    st.session_state.data["rel_a"] = a
    st.session_state.data["rel_b"] = b

    # 문제 8
    st.session_state.data["sq1"] = random.randint(10, 80)

    # 문제 9
    while True:
        sq2 = random.randint(20, 100)
        need = get_needed_number_for_square(sq2)
        if need != 1 and need != sq2:
            break
    st.session_state.data["sq2"] = sq2

    # 문제 10
    st.session_state.data["limit_n"] = random.randint(50, 150)
    st.session_state.data["m1"] = random.randint(2, 5)
    st.session_state.data["m2"] = random.randint(6, 9)

#-------------------------------------------------
# 화면 타이틀
#-------------------------------------------------
st.markdown("<div class='big-title'>🎓 중1 수학 소인수분해 퀴즈</div>", unsafe_allow_html=True)
st.markdown("---")

step = st.session_state.step

#-------------------------------------------------
# 문제 화면
#-------------------------------------------------
def show_input_problem(title, question, key):
    st.markdown(f"<div class='sub-card'><h4>{title}</h4><p>{question}</p></div>", unsafe_allow_html=True)
    st.session_state.answers[key] = st.text_input("정답:", key=key)

if step <= 10:
    if step == 1:
        show_input_problem("[문제 1]", f"숫자 {st.session_state.data['num1']}을(를) 소인수분해 하세요 (예: 2^3 * 5)", "q1")
    elif step == 2:
        c1, c2 = st.session_state.data["c1"], st.session_state.data["c2"]
        show_input_problem("[문제 2]", f"{c1}, {c2}은(는) 서로소입니까? (맞으면 1, 아니면 0)", "q2")
    elif step == 3:
        g1, g2 = st.session_state.data["g1"], st.session_state.data["g2"]
        show_input_problem("[문제 3]", f"{g1}, {g2}의 최대공약수?", "q3")
    elif step == 4:
        cd1, cd2 = st.session_state.data["cd1"], st.session_state.data["cd2"]
        show_input_problem("[문제 4]", f"{cd1}, {cd2}의 공약수 개수?", "q4")
    elif step == 5:
        l1, l2 = st.session_state.data["l1"], st.session_state.data["l2"]
        show_input_problem("[문제 5]", f"{l1}, {l2}의 최소공배수?", "q5")
    elif step == 6:
        a, b = st.session_state.data["bus_a"], st.session_state.data["bus_b"]
        show_input_problem("[문제 6]", f"A={a}분, B={b}분 버스가 동시에 출발. 몇 분 뒤에 처음 만날까요?", "q6")
    elif step == 7:
        a, b = st.session_state.data["rel_a"], st.session_state.data["rel_b"]
        gcd_val = math.gcd(a,b)
        show_input_problem("[문제 7]", f"두 자연수 곱={a*b}, 최대공약수={gcd_val}. 최소공배수는?", "q7")
    elif step == 8:
        n = st.session_state.data["sq1"]
        show_input_problem("[문제 8]", f"{n} × x 가 제곱수가 되도록 할 때 x의 최소값은?", "q8")
    elif step == 9:
        n = st.session_state.data["sq2"]
        show_input_problem("[문제 9]", f"{n} ÷ a 가 제곱수가 되도록 하는 최소 a는?", "q9")
    elif step == 10:
        N = st.session_state.data["limit_n"]
        m1, m2 = st.session_state.data["m1"], st.session_state.data["m2"]
        show_input_problem("[문제 10]", f"1~{N} 중 {m1} 또는 {m2}의 배수 개수?", "q10")

    if st.button("다음 문제"):
        st.session_state.step += 1
        st.experimental_rerun()

#-------------------------------------------------
# 결과 화면
#-------------------------------------------------
else:
    st.markdown("<div class='big-title'>📊 최종 결과</div>", unsafe_allow_html=True)
    total_score = 0
    correct_list = []
    wrong_list = []

    # 문제별 채점
    # 문제 1
    if check_factorization(st.session_state.answers.get("q1",""), st.session_state.data["num1"]):
        total_score += 10
        correct_list.append(1)
    else:
        wrong_list.append(1)

    # 문제 2
    c1, c2 = st.session_state.data["c1"], st.session_state.data["c2"]
    ans2 = 1 if math.gcd(c1,c2)==1 else 0
    if str(st.session_state.answers.get("q2","")) == str(ans2):
        total_score += 10
        correct_list.append(2)
    else:
        wrong_list.append(2)

    # 문제 3
    g1, g2 = st.session_state.data["g1"], st.session_state.data["g2"]
    ans3 = math.gcd(g1,g2)
    if str(st.session_state.answers.get("q3","")) == str(ans3):
        total_score += 10
        correct_list.append(3)
    else:
        wrong_list.append(3)

    # 문제 4
    cd1, cd2 = st.session_state.data["cd1"], st.session_state.data["cd2"]
    ans4 = get_divisor_count(math.gcd(cd1, cd2))
    if str(st.session_state.answers.get("q4","")) == str(ans4):
        total_score += 10
        correct_list.append(4)
    else:
        wrong_list.append(4)

    # 문제 5
    l1, l2 = st.session_state.data["l1"], st.session_state.data["l2"]
    ans5 = (l1*l2)//math.gcd(l1,l2)
    if str(st.session_state.answers.get("q5","")) == str(ans5):
        total_score += 10
        correct_list.append(5)
    else:
        wrong_list.append(5)

    # 문제 6
    a,b = st.session_state.data["bus_a"], st.session_state.data["bus_b"]
    ans6 = (a*b)//math.gcd(a,b)
    if str(st.session_state.answers.get("q6","")) == str(ans6):
        total_score += 10
        correct_list.append(6)
    else:
        wrong_list.append(6)

    # 문제 7
    a,b = st.session_state.data["rel_a"], st.session_state.data["rel_b"]
    ans7 = (a*b)//math.gcd(a,b)
    if str(st.session_state.answers.get("q7","")) == str(ans7):
        total_score += 10
        correct_list.append(7)
    else:
        wrong_list.append(7)

    # 문제 8
    n = st.session_state.data["sq1"]
    ans8 = get_needed_number_for_square(n)
    if str(st.session_state.answers.get("q8","")) == str(ans8):
        total_score += 10
        correct_list.append(8)
    else:
        wrong_list.append(8)

    # 문제 9
    n = st.session_state.data["sq2"]
    ans9 = get_needed_number_for_square(n)
    if str(st.session_state.answers.get("q9","")) == str(ans9):
        total_score += 10
        correct_list.append(9)
    else:
        wrong_list.append(9)

    # 문제 10
    N = st.session_state.data["limit_n"]
    m1, m2 = st.session_state.data["m1"], st.session_state.data["m2"]
    lcm = (m1*m2)//math.gcd(m1,m2)
    ans10 = (N//m1) + (N//m2) - (N//lcm)
    if str(st.session_state.answers.get("q10","")) == str(ans10):
        total_score += 10
        correct_list.append(10)
    else:
        wrong_list.append(10)

    st.markdown(f"<div class='result-card'><h3>총점: {total_score} / 100점</h3></div>", unsafe_allow_html=True)
    st.write(f"⭕ 맞은 문제: {correct_list}")
    st.write(f"❌ 틀린 문제: {wrong_list}")

    st.session_state.record.append(total_score)

    if st.button("다시 시작"):
        for key in ["step", "answers", "data", "initialized"]:
            del st.session_state[key]
        st.experimental_rerun()
