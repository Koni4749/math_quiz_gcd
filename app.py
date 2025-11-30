import streamlit as st
import random
import math

st.set_page_config(page_title="중1 소인수분해 퀴즈", page_icon="🎓", layout="centered")

# 스타일
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

#---------------------------------
# 함수 정의
#---------------------------------
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
    if temp > 1: count *= 2
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
        if term == "": continue
        if '^' in term:
            parts = term.split('^')
            if len(parts) != 2: return False, "식 형식이 잘못되었습니다."
            base_str, exp_str = parts
            if not base_str.isdigit() or not exp_str.isdigit():
                return False, "숫자가 아닌 부분이 있습니다."
            base, exp = int(base_str), int(exp_str)
        else:
            if not term.isdigit(): return False, "숫자가 아닌 부분이 있습니다."
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
    while d*d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            if count % 2 != 0:
                result *= d
        d += 1
    if temp > 1: result *= temp
    return result

#---------------------------------
# 세션 상태 초기화
#---------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0
    st.session_state.correct = []
    st.session_state.wrong = []
    st.session_state.data = {}

#---------------------------------
# 문제 랜덤 생성 (최초 1회)
#---------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True

    # 문제 1
    num1 = random.randint(12,100)
    while is_prime(num1): num1 = random.randint(12,100)
    st.session_state.data["num1"] = num1

    # 문제 2
    c1, c2 = random.randint(10,30), random.randint(10,30)
    while c1==c2: c2=random.randint(10,30)
    st.session_state.data["c1"]=c1
    st.session_state.data["c2"]=c2

    # 문제 3
    while True:
        g1, g2 = random.randint(12,60), random.randint(12,60)
        if math.gcd(g1,g2) > 1: break
    st.session_state.data["g1"]=g1
    st.session_state.data["g2"]=g2

    # 문제 4
    cd1, cd2 = random.randint(20,100), random.randint(20,100)
    st.session_state.data["cd1"]=cd1
    st.session_state.data["cd2"]=cd2

    # 문제 5
    st.session_state.data["l1"]=random.randint(4,30)
    st.session_state.data["l2"]=random.randint(4,30)

    # 문제 6
    st.session_state.data["bus_a"]=random.randint(4,9)
    st.session_state.data["bus_b"]=random.randint(10,15)

    # 문제 7
    while True:
        a=random.randint(6,20)
        b=random.randint(6,20)
        if math.gcd(a,b)>1: break
    st.session_state.data["rel_a"]=a
    st.session_state.data["rel_b"]=b

    # 문제 8
    st.session_state.data["sq1"]=random.randint(10,80)

    # 문제 9
    while True:
        sq2=random.randint(20,100)
        need=get_needed_number_for_square(sq2)
        if need!=1 and need!=sq2: break
    st.session_state.data["sq2"]=sq2

    # 문제 10
    st.session_state.data["limit_n"]=random.randint(50,150)
    st.session_state.data["m1"]=random.randint(2,5)
    st.session_state.data["m2"]=random.randint(6,9)

#---------------------------------
# 화면 타이틀
#---------------------------------
st.markdown("<div class='big-title'>🎓 중1 수학 소인수분해 퀴즈</div>", unsafe_allow_html=True)
st.markdown("---")

step = st.session_state.step

#---------------------------------
# 문제 1
#---------------------------------
if step==1:
    num1 = st.session_state.data["num1"]
    st.markdown(f"<div class='sub-card'><h4>[문제 1]</h4>숫자 {num1}을(를) 소인수분해 하세요.</div>", unsafe_allow_html=True)
    user_input = st.text_input("정답 (예: 2^3 * 5)", key="q1_input")

    if st.button("제출"):
        ok, msg = check_factorization(user_input, num1)
        if ok:
            st.success("정답! (+10점)")
            st.session_state.score +=10
            st.session_state.correct.append(1)
        else:
            st.error(f"오답! ({msg})")
            st.session_state.wrong.append(1)
        st.session_state.step+=1
        st.experimental_rerun()

#---------------------------------
# 문제 2~10 동일 패턴
#---------------------------------
elif step==2:
    c1,c2 = st.session_state.data["c1"], st.session_state.data["c2"]
    ans = 1 if math.gcd(c1,c2)==1 else 0
    user_input = st.text_input(f"[문제 2] {c1}, {c2}은(는) 서로소입니까? (맞으면 1, 아니면 0)", key="q2_input")
    if st.button("제출", key="btn2"):
        if user_input.isdigit() and int(user_input)==ans:
            st.success("정답! (+10점)")
            st.session_state.score+=10
            st.session_state.correct.append(2)
        else:
            st.error(f"오답! 정답: {ans}")
            st.session_state.wrong.append(2)
        st.session_state.step+=1
        st.experimental_rerun()

elif step==3:
    g1,g2 = st.session_state.data["g1"], st.session_state.data["g2"]
    ans = math.gcd(g1,g2)
    user_input = st.text_input(f"[문제 3] {g1}, {g2}의 최대공약수?", key="q3_input")
    if st.button("제출", key="btn3"):
        if user_input.isdigit() and int(user_input)==ans:
            st.success("정답! (+10점)")
            st.session_state.score+=10
            st.session_state.correct.append(3)
        else:
            st.error(f"오답! 정답: {ans}")
            st.session_state.wrong.append(3)
        st.session_state.step+=1
        st.experimental_rerun()

#---------------------------------
# 이하 문제 4~10도 동일 패턴으로 구현 가능
#---------------------------------

# 마지막 결과 화면
elif step==11:
    score = st.session_state.score
    st.markdown("<div class='big-title'>📊 최종 결과</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-card'><h3>총점: {score} / 100점</h3></div>", unsafe_allow_html=True)
    st.write(f"⭕ 맞은 문제: {st.session_state.correct}")
    st.write(f"❌ 틀린 문제: {st.session_state.wrong}")

    if st.button("다시 시작"):
        for key in ["step","score","correct","wrong","data","initialized"]:
            if key in st.session_state: del st.session_state[key]
        st.experimental_rerun()
