import streamlit as st
import random
import math
import pandas as pd

st.set_page_config(page_title="중1 소인수분해 퀴즈", page_icon="🎓", layout="centered")

# 스타일 개선
st.markdown("""
<style>
    .big-title { font-size:35px; font-weight:700; text-align:center; }
    .sub-card { 
        padding:20px; 
        background:#f7f7f9; 
        border-radius:10px;  
        border:1px solid #ddd; 
    }
    .result-card {
        padding:25px; 
        background:#eef9ff; 
        border-radius:10px;  
        border:2px solid #40a6ff; 
    }
</style>
""", unsafe_allow_html=True)


#-------------------------------------------------
# 기존 함수들 (그대로)
#-------------------------------------------------
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_divisor_count(n):
    count = 1
    d = 2
    temp = n
    while d * d <= temp:
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
        return False, "입력값이 없습니다."
    allowed = set("0123456789*^")
    if not set(clean_str).issubset(allowed):
        return False, "숫자와 기호(*, ^)만 입력해주세요."

    terms = clean_str.split('*')
    calculated_value = 1

    for term in terms:
        if term == "":
            continue
        if '^' in term:
            parts = term.split('^')
            if len(parts) != 2:
                return False, "식 형식이 잘못되었습니다."
            base_str, exp_str = parts[0], parts[1]
            if not base_str.isdigit() or not exp_str.isdigit():
                return False, "숫자가 아닌 부분이 있습니다."
            base, exp = int(base_str), int(exp_str)
        else:
            if not term.isdigit():
                return False, "숫자가 아닌 부분이 있습니다."
            base, exp = int(term), 1

        if not is_prime(base):
            return False, f"'{base}'은(는) 소수가 아닙니다."

        calculated_value *= (base ** exp)

    if calculated_value == target_num:
        return True, "정답"
    return False, "계산 결과가 틀립니다."

def get_needed_number_for_square(n):
    result = 1
    d = 2
    temp = n
    while d * d <= temp:
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
# 세션 상태 (진행상황)
#-------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0
    st.session_state.correct = []
    st.session_state.wrong = []
    st.session_state.data = {}
    st.session_state.record = []   # 기록 저장 (추가 기능)

#-------------------------------------------------
# 최초 랜덤값 생성
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


#-------------------------------------
# 화면 타이틀
#-------------------------------------
st.markdown("<div class='big-title'>🎓 중1 수학 소인수분해 퀴즈</div>", unsafe_allow_html=True)
st.markdown("---")

step = st.session_state.step


#-------------------------------------
# 반복되는 문제 UI 출력 함수
#-------------------------------------
def show_problem(title, question, answer, key):
    st.markdown(f"<div class='sub-card'><h4>{title}</h4><p>{question}</p></div>", unsafe_allow_html=True)
    user = st.text_input("정답:", key=key)
    if st.button("제출", key=f"btn{key}"):
        if user.isdigit() and int(user) == answer:
            st.success("정답! (+10점)")
            st.session_state.score += 10
            st.session_state.correct.append(step)
        else:
            st.error(f"오답! 정답은 {answer}")
            st.session_state.wrong.append(step)
        st.session_state.step += 1
        st.rerun()


#-------------------------------------
# 문제별 출력
#-------------------------------------
if step == 1:
    num1 = st.session_state.data["num1"]
    st.markdown(f"<div class='sub-card'><h4>[문제 1]</h4>숫자 {num1}을(를) 소인수분해 하세요.</div>", unsafe_allow_html=True)
    user = st.text_input("정답 (예: 2^3 * 5)")

    if st.button("제출"):
        ok, msg = check_factorization(user, num1)
        if ok:
            st.success("정답! (+10점)")
            st.session_state.score += 10
            st.session_state.correct.append(1)
        else:
            st.error(f"오답! ({msg})")
            st.session_state.wrong.append(1)
        st.session_state.step += 1
        st.rerun()


elif step == 2:
    c1, c2 = st.session_state.data["c1"], st.session_state.data["c2"]
    ans = 1 if math.gcd(c1, c2) == 1 else 0
    show_problem("[문제 2]", f"{c1}, {c2}은(는) 서로소입니까? (맞으면 1, 아니면 0)", ans, "q2")

elif step == 3:
    g1, g2 = st.session_state.data["g1"], st.session_state.data["g2"]
    ans = math.gcd(g1, g2)
    show_problem("[문제 3]", f"{g1}, {g2}의 최대공약수?", ans, "q3")

elif step == 4:
    cd1, cd2 = st.session_state.data["cd1"], st.session_state.data["cd2"]
    ans = get_divisor_count(math.gcd(cd1, cd2))
    show_problem("[문제 4]", f"{cd1}, {cd2}의 공약수 개수?", ans, "q4")

elif step == 5:
    l1, l2 = st.session_state.data["l1"], st.session_state.data["l2"]
    ans = (l1 * l2) // math.gcd(l1, l2)
    show_problem("[문제 5]", f"{l1}, {l2}의 최소공배수?", ans, "q5")

elif step == 6:
    a, b = st.session_state.data["bus_a"], st.session_state.data["bus_b"]
    ans = (a * b) // math.gcd(a, b)
    show_problem("[문제 6]",
        f"A={a}분, B={b}분 버스가 동시에 출발. 몇 분 뒤에 처음 만날까요?",
        ans, "q6")

elif step == 7:
    a, b = st.session_state.data["rel_a"], st.session_state.data["rel_b"]
    gcd_val = math.gcd(a, b)
    ans = (a * b) // gcd_val
    show_problem("[문제 7]",
        f"두 자연수 곱={a*b}, 최대공약수={gcd_val}. 최소공배수는?",
        ans, "q7")

elif step == 8:
    n = st.session_state.data["sq1"]
    ans = get_needed_number_for_square(n)
    show_problem("[문제 8]", f"{n} × x 가 제곱수가 되도록 할 때 x의 최소값은?", ans, "q8")

elif step == 9:
    n = st.session_state.data["sq2"]
    ans = get_needed_number_for_square(n)
    show_problem("[문제 9]", f"{n} ÷ a 가 제곱수가 되도록 하는 최소 a는?", ans, "q9")

elif step == 10:
    N = st.session_state.data["limit_n"]
    m1, m2 = st.session_state.data["m1"], st.session_state.data["m2"]
    lcm = (m1 * m2) // math.gcd(m1, m2)
    ans = (N//m1) + (N//m2) - (N//lcm)
    show_problem("[문제 10]", f"1~{N} 중 {m1} 또는 {m2}의 배수 개수?", ans, "q10")


#-------------------------------------
# 결과 + 기록저장 (그래프 제거)
#-------------------------------------
elif step == 11:
    score = st.session_state.score

    st.markdown("<div class='big-title'>📊 최종 결과</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-card'><h3>총점: {score} / 100점</h3></div>", unsafe_allow_html=True)
    
    st.write(f"⭕ 맞은 문제: {st.session_state.correct}")
    st.write(f"❌ 틀린 문제: {st.session_state.wrong}")

    # 점수 기록 저장
    st.session_state.record.append(score)

    # CSV 저장 버튼
    if st.button("CSV로 기록 다운로드"):
        df = pd.DataFrame({"score": st.session_state.record})
        st.download_button("📥 CSV 다운로드", df.to_csv(index=False), "scores.csv")

    # 다시 시작 버튼
    if st.button("다시 하기"):
        for key in ["step", "score", "correct", "wrong", "data", "initialized"]:
            del st.session_state[key]
        st.rerun()
