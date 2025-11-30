import streamlit as st
import random
import math

st.set_page_config(page_title="중1 소인수분해 퀴즈", page_icon="🎓", layout="wide")

# 스타일
st.markdown("""
<style>
.big-title { font-size:35px; font-weight:700; text-align:center; }
.sub-card { padding:20px; background:#f7f7f9; border-radius:10px; border:1px solid #ddd; margin-bottom:20px; }
.result-card { padding:25px; background:#eef9ff; border-radius:10px; border:2px solid #40a6ff; margin-bottom:20px; }
</style>
""", unsafe_allow_html=True)

#-------------------------------------------------
# 함수 정의
#-------------------------------------------------
def is_prime(n):
    if n < 2: return False
    for i in range(2,int(n**0.5)+1):
        if n % i == 0: return False
    return True

def check_factorization(user_str, target_num):
    clean_str = user_str.replace(" ","").lower().replace("x","*")
    if not clean_str: return False
    allowed = set("0123456789*^")
    if not set(clean_str).issubset(allowed): return False

    terms = clean_str.split('*')
    value = 1
    for t in terms:
        if not t: continue
        if '^' in t:
            parts = t.split('^')
            if len(parts)!=2 or not parts[0].isdigit() or not parts[1].isdigit(): return False
            base, exp = int(parts[0]), int(parts[1])
        else:
            if not t.isdigit(): return False
            base, exp = int(t), 1
        if not is_prime(base): return False
        value *= base**exp
    return value == target_num

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
            if count %2 !=0:
                result *= d
        d += 1
    if temp > 1:
        result *= temp
    return result

def get_divisor_count(n):
    count = 1
    d = 2
    temp = n
    while d*d <= temp:
        if temp % d ==0:
            exp =0
            while temp%d==0:
                exp +=1
                temp//=d
            count*=(exp+1)
        d+=1
    if temp>1:
        count*=2
    return count

#-------------------------------------------------
# 세션 초기화
#-------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.answers = {}
    st.session_state.data = {}
    st.session_state.initialized = False

#-------------------------------------------------
# 문제 데이터 생성
#-------------------------------------------------
if not st.session_state.initialized:
    st.session_state.initialized = True
    data = st.session_state.data

    # 문제 1
    n1 = random.randint(12,100)
    while is_prime(n1): n1=random.randint(12,100)
    data["num1"] = n1

    # 문제 2
    c1,c2=random.randint(10,30),random.randint(10,30)
    while c1==c2: c2=random.randint(10,30)
    data["c1"],data["c2"]=c1,c2

    # 문제 3
    while True:
        g1,g2=random.randint(12,60),random.randint(12,60)
        if math.gcd(g1,g2)>1: break
    data["g1"],data["g2"]=g1,g2

    # 문제 4
    cd1,cd2=random.randint(20,100),random.randint(20,100)
    data["cd1"],data["cd2"]=cd1,cd2

    # 문제 5
    data["l1"],data["l2"]=random.randint(4,30),random.randint(4,30)

    # 문제 6
    data["bus_a"],data["bus_b"]=random.randint(4,9),random.randint(10,15)

    # 문제 7
    while True:
        a,b=random.randint(6,20),random.randint(6,20)
        if math.gcd(a,b)>1: break
    data["rel_a"],data["rel_b"]=a,b

    # 문제 8
    data["sq1"]=random.randint(10,80)

    # 문제 9
    while True:
        sq2=random.randint(20,100)
        need=get_needed_number_for_square(sq2)
        if need!=1 and need!=sq2: break
    data["sq2"]=sq2

    # 문제 10
    data["limit_n"]=random.randint(50,150)
    data["m1"]=random.randint(2,5)
    data["m2"]=random.randint(6,9)

#-------------------------------------------------
# UI
#-------------------------------------------------
st.markdown("<div class='big-title'>🎓 중1 수학 소인수분해 퀴즈</div>",unsafe_allow_html=True)
st.markdown("---")

def show_input(title, question, key):
    st.markdown(f"<div class='sub-card'><h4>{title}</h4><p>{question}</p></div>",unsafe_allow_html=True)
    st.session_state.answers[key]=st.text_input("정답:",key=key)

# 문제 출력
if st.session_state.step<=10:
    step=st.session_state.step
    d=st.session_state.data

    if step==1:
        show_input("[문제 1]",f"숫자 {d['num1']} 소인수분해 (예: 2^3 * 5)","q1")
    elif step==2:
        show_input("[문제 2]",f"{d['c1']},{d['c2']} 서로소? 맞으면1, 아니면0","q2")
    elif step==3:
        show_input("[문제 3]",f"{d['g1']},{d['g2']} 최대공약수","q3")
    elif step==4:
        show_input("[문제 4]",f"{d['cd1']},{d['cd2']} 공약수 개수","q4")
    elif step==5:
        show_input("[문제 5]",f"{d['l1']},{d['l2']} 최소공배수","q5")
    elif step==6:
        show_input("[문제 6]",f"A={d['bus_a']}분,B={d['bus_b']}분 버스 처음 만나는 시간","q6")
    elif step==7:
        gcd_val=math.gcd(d['rel_a'],d['rel_b'])
        show_input("[문제 7]",f"두 자연수 곱={d['rel_a']*d['rel_b']}, 최대공약수={gcd_val}. 최소공배수?","q7")
    elif step==8:
        show_input("[문제 8]",f"{d['sq1']} × x가 제곱수가 되도록 최소 x","q8")
    elif step==9:
        show_input("[문제 9]",f"{d['sq2']} ÷ a가 제곱수가 되도록 최소 a","q9")
    elif step==10:
        show_input("[문제 10]",f"1~{d['limit_n']} 중 {d['m1']} 또는 {d['m2']} 배수 개수","q10")

    if st.button("다음 문제"):
        st.session_state.step+=1
        st.experimental_rerun()

# 결과 화면
else:
    st.markdown("<div class='big-title'>📊 최종 결과</div>",unsafe_allow_html=True)
    total_score=0
    correct_list=[]
    wrong_list=[]
    d=st.session_state.data
    a=st.session_state.answers

    # 문제 1
    if check_factorization(a.get("q1",""),d['num1']): total_score+=10; correct_list.append(1)
    else: wrong_list.append(1)

    # 문제 2
    ans2=1 if math.gcd(d['c1'],d['c2'])==1 else 0
    if str(a.get("q2",""))==str(ans2): total_score+=10; correct_list.append(2)
    else: wrong_list.append(2)

    # 문제 3
    ans3=math.gcd(d['g1'],d['g2'])
    if str(a.get("q3",""))==str(ans3): total_score+=10; correct_list.append(3)
    else: wrong_list.append(3)

    # 문제 4
    ans4=get_divisor_count(math.gcd(d['cd1'],d['cd2']))
    if str(a.get("q4",""))==str(ans4): total_score+=10; correct_list.append(4)
    else: wrong_list.append(4)

    # 문제 5
    ans5=(d['l1']*d['l2'])//math.gcd(d['l1'],d['l2'])
    if str(a.get("q5",""))==str(ans5): total_score+=10; correct_list.append(5)
    else: wrong_list.append(5)

    # 문제 6
    ans6=(d['bus_a']*d['bus_b'])//math.gcd(d['bus_a'],d['bus_b'])
    if str(a.get("q6",""))==str(ans6): total_score+=10; correct_list.append(6)
    else: wrong_list.append(6)

    # 문제 7
    ans7=(d['rel_a']*d['rel_b'])//math.gcd(d['rel_a'],d['rel_b'])
    if str(a.get("q7",""))==str(ans7): total_score+=10; correct_list.append(7)
    else: wrong_list.append(7)

    # 문제 8
    ans8=get_needed_number_for_square(d['sq1'])
    if str(a.get("q8",""))==str(ans8): total_score+=10; correct_list.append(8)
    else: wrong_list.append(8)

    # 문제 9
    ans9=get_needed_number_for_square(d['sq2'])
    if str(a.get("q9",""))==str(ans9): total_score+=10; correct_list.append(9)
    else: wrong_list.append(9)

    # 문제 10
    lcm=(d['m1']*d['m2'])//math.gcd(d['m1'],d['m2'])
    ans10=(d['limit_n']//d['m1'])+(d['limit_n']//d['m2'])-(d['limit_n']//lcm)
    if str(a.get("q10",""))==str(ans10): total_score+=10; correct_list.append(10)
    else: wrong_list.append(10)

    st.markdown(f"<div class='result-card'><h3>총점: {total_score}/100점</h3></div>",unsafe_allow_html=True)
    st.write(f"⭕ 맞은 문제: {correct_list}")
    st.write(f"❌ 틀린 문제: {wrong_list}")

    if st.button("다시 시작"):
        for key in ["step","answers","data","initialized"]:
            del st.session_state[key]
        st.experimental_rerun()
