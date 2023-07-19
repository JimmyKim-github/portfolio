# 원본 제작자 : 메이플 인벤 '시먹' 님 2023.07.14 제작 https://www.inven.co.kr/board/maple/2304/34906

import numpy as np
import itertools

# 'n'은 현재 몇 번의 강화가 진행 되었는지를 의미함. 최대 20
# 'm'은 현재 main stat 레벨을 의미함. 최대 10

print('[2023.07 ver. 메이플스토리 헥사스텟 시뮬레이터]','\n')

##### 1. 기본 상수들
#p[m]은 main stat이 m레벨인 상태에서 강화를 했을 때 main stat level에 붙을 확률을 의미함. m은 0부터 10
p=np.array([0.35, 0.35, 0.35, 0.2, 0.2, 0.2, 0.2, 0.15, 0.1, 0.05, 0])
#s[m]은 m번 강화된 상태에서 강화를 했을 때 stat 강화를 위해 필요한 솔에르다 조각의 개수를 의미함. m은 0부터 10
#나무위키에 m=10일 때 값이 안 나와서 일단 임의로 50 넣었음. 추후 수정
s=np.array([10, 10, 10, 20, 20, 20, 20, 30, 40, 50, 50])
#cr은 초기화 비용을 의미함. 단위는 만 메소임. 즉 sr은 천만 메소
cr=1000

##### 2. 입력상수
#cs는 솔에르다조각 하나의 메소가격을 의미함. 단위는 만 메소임.
#cs=1000
#o는 목표로하는 main stat 강화 레벨을 의미함. 어차피 5이상은 볼거니까 5부터 10까지 넣으면 됨. 예외처리 귀찮아....
#o=10
while True:
    cs = input("[필수] Q1. 솔 에르다 조각 메소가격 입력 해주세요 단위는 만 메소로!!: ")
    if not cs.isdigit():
        print("숫자만 입력 해주세요.ㅠㅠ")
        continue
    cs = int(cs)
    if cs < 0:
        print("숫자를 입력해주세요.")
        continue
    break
while True:
    o = input("[필수] Q2. 목표로 하는 '헥사 스탯의 메인 스탯'을 숫자로만 입력 해주세요 0~10 이내로!!: ")
    if not o.isdigit():
        print("숫자를 입력해주세요.")
        continue
    o = int(o)
    if o < 0 or o > 10:
        print("입력 값이 범위가 초과 되었습니다. 0부터 10 사이의 값을 입력해주세요.")
        continue
    break
hexa = str(cs) + str(o)

print('\n', "<<입력하신 헥사스탯 시뮬레이션 결과 입니다.>>")

##### 3 강화 전략 정의
#전략은 다음과 같은 방식으로 결정됨. n번 강화했을 때 main stat 강화수치 m<=r[n]이면 강화를 중단하고 처음부터 다시시작함
#r[n]의 조건들은 아래와 같음.
    #3.1.1 -1<=r[n] // m은 항상 0이상이기때문에 -1보다 작은 r[n]은 전부 똑같음.
    #                  그냥 n번 강화 까지는 절대 포기안할거야 라는 말이 r[n]=-1임. 초기화가 n>=10부터 가능하므로 r[0~10]=-1로 가정함
    #                  아래 3.1.2~3.1.5는 n>=10이상인 경우에만 해당함.
    #3.1.2 r[n]<o // 강화가 목표 수치인 o에 도달하면 초기화할 필요가 없음
    #3.1.3 (o+n-21)<=r[n] // 앞으로 강화횟수가 (20-n)번 남았는데 다붙어도 목표인 o에 도달할 수 없기 때문/ 위 조건과 합쳐져 r[20]=0-1
    #3.1.4 If n1<n2, then r[n1]<=r[n2] // 10번중 5번 붙으면 포기할건데 11번중 4번 붙은건 포기안하면 이상하니까
    #3.1.5 r[n+1]-r[n]=0 or 1 // 10번중 4번 붙은건 포기안하는데 11번중 5번 붙은건 포기할거라는게 말이안됨

#위 조건들을 만족하는 r[n]을 중복없이 모두 고르는 방법은 다음과 같음
    #3.1.7 우선 r[10]값을 고름 이 값을 r10이라고 하자. r10의 범위는 -1<=r10<o 임.
    #3.1.7 10부터19까지의 숫자중 중복없이 순서에 상관없이 o-1-r10개의 숫자를 선택함. 이 숫자들에 해당하는 r[n+1]-r[n]=1로 만들거임.
    #3.1.8 그 숫자를 크기가 작은순으로 N[10],...,N[o+8-r10]라고 가정하자.
    #3.1.9 r[0]~r[N[10]-10]=r10 && r[N[i]+1]~r[N[i+1]]=i+1+r10 for i=10,...,o-3-r10 && r[N[o-2-r10]+1]~r[10]=o-1

# 위에서 말한대로 nN개의 강화 전략이 만들어짐.

N=[]
for r10 in range(-1,o):
    arr=[n for n in range(10,20)]
    Nm=list(itertools.combinations(arr,o-r10-1))
    N.extend(Nm)
nN=len(N)

##무지성 강화 정의: main stat이 o강에 도달할 가능성이 존재만 한다면 무조건 강화하는 것을 의미(결과비교용)
rm=[o-1-20+n if n>=20-o+1 else -1 for n in range(21)]

##### 4 강화 전략별 기댓값 탐색 시작
##c는 강화전략별 소모메소 기댓값을 의미함. 나중에 최적의 강화전략을 찾기 위해 사용. 우선은 초기화
##rn은 강화전략별 초기화 횟수 기댓값을 의미함.
##rn은 강화전략별 솔 에르다 조각의 소모 기댓값을 의미함.
c=np.zeros(nN)
rn=np.zeros(nN)
sn=np.zeros(nN)
for i in range(nN):
    ##4.1 강화 전략 N[i]로 부터 r[n]을 생성 (3.1.9 참조)
    r10=o-len(N[i])-1
    Ni=np.array(N[i])
    r=np.array([-1 for n in range(21)],dtype=int)
    if Ni.shape[0]==0:
        for j in range(10,21):
            r[j]=r10
    else:       
        for j in range(10,Ni[0]+1):
            r[j]=r10
        for j in range(0,o-2-r10):
            for k in range(Ni[j]+1,Ni[j+1]+1):
                r[k]=r10+j+1
        for j in range(Ni[o-2-r10]+1,21):
            r[j]=o-1
            
    ##본 방법이 무지성 강화에 해당하는지 체크
    if list(r)==rm:
        im=i
    
    ##4.2 강화 전략 N[i]로 목표 o를 달성하는데 소모하는 메소의 기댓값 계산
    #cm[n][m]을 현재 n번강화에서 m번 main stat에 붙은상황이고, 여기서 강화를 진행해 목표를 달성할때까지의 소모메소 기댓값이라 하자.
    #이때 n<=10인경우 0<=m<=n이다.
    #그리고 n>=11인경우 max(0,r[n])<=m<=10이다. 강화전략 상 다른 경우는 이미 초기화해버렸기 때문에 존재할 수 없음
    #위에서 왼쪽 등호는 n이 N[i]의 원소일때만 가능 왜냐하면 10개중 5개를 초기화했다면 11개중 5개인 상황은 나올 수 없기 때문.
    ##r2[n]과 r3[n]은 위 조건들을 고려하여 가능한 (n,m)의 조합이 r2[n]<=m<=r3[n]이 되도록 만든 식이다.
    r2=np.zeros(21,dtype=int)
    r3=np.array([np.min([10,n]) for n in range(21)])
    r2[11:21]=r[11:21]+1
    for j in range(o-1-r10):
        r2[Ni[j]+1]-=1

  
    ##4.3 강화 전략 N[i]로 목표 o를 달성하는데 소모하는 메소의 기댓값 계산
    #세가지경우를 생각하자.
    #(n>10 and m=r[n]인 경우) or (n=10 m<r[10])인 경우)(4.3.1)와 (20,m>=o)인 경우(4.3.2)와 n<19이고 r[n]<m<=r3[n]인 경우(4.3.3)
     #4.3.1 cm[n][m]=cr+cm[0][0] /초기화를 하고 다시 (n,m)=(0,0)인 경우로 가기 때문
     #4.3.2 cm[20][m]=0 /목표를 이미 달성했기때문에 기댓값은 0.
     #4.3.3 cm[n][m]=cs*s[m]+cm[n+1][m+1]*p[m]+cm[n+1][m]*(1-p[m]) /설명은 밑 참조. (cm[n+1][11]은 어차피 p[10]=0이므로 고려안함) 
      #첫번째 term은 강화비용
      #두번째 term은 성공하는 경우
      #세번째 term은 실패하는 경우
    #위 연립 방정식을 연립해서 cm[0][0]을 계산하면 됨.
    #위 연립 방정식을 행렬을 이용해서 풀기 위해 reindexing을 진행하겠음. (n,m)을 k로 대응시켜 cm[n][m]을 cmk[k]로 변환
    #ktonm[k]=[n,m],nmtok[n,m]=k, ks는 총 k의 개수
    #4.3.1, 4.3.2, 4.3.3로 이루어진 연립방정식을 cmk=A*cmk+b로 변환.
    nmtok=np.zeros([21,11],dtype=int)
    ktonm=[]
    kindex=0
    for n in range (0,21):
        for m in range(r2[n],r3[n]+1):
            nmtok[n][m]=kindex
            ktonm.append([n,m])
            kindex+=1
    A=np.zeros([kindex,kindex])
    b=np.zeros([kindex])
    
    
    ##4.4초기화 횟수의 기댓값 계산
    #rnm[n][m]을 메소의 기댓값과 비슷한 방식으로 앞으로 초기화할 횟수의 기댓값이라 가정
    #위와 똑같이 세가지경우를 생각하자.
    #(n>10 and m=r[n]인 경우) or (n=10 m<r[10])인 경우)(4.3.1)와 (20,m>=o)인 경우(4.3.2)와 n<19이고 r[n]<m<=r3[n]인 경우(4.3.3)
     #4.4.1 rnm[n][m]=1+rnm[0][0]
     #4.4.2 rnm[20][m]=0 
     #4.4.3 rnm[n][m]=rnm[n+1][m+1]*p[m]+rnm[n+1][m]*(1-p[m])
    #위 연립 방정식을 연립해서 rnm[0][0]을 계산하면 됨. reindexing 똑같이해서 rnmk도 만듬
    #4.4.1, 4.4.2, 4.4.3로 이루어진 연립방정식을 rnmk=A*rnmk+b2로 변환.  (A행렬은 동일함)
    
    b2=np.zeros([kindex])
    
    ##4.5사용 조각 수의
    #snm[n][m]을 메소의 기댓값과 비슷한 방식으로 앞으로 초기화할 횟수의 기댓값이라 가정
    #위와 똑같이 세가지경우를 생각하자.
    #(n>10 and m=r[n]인 경우) or (n=10 m<r[10])인 경우)(4.3.1)와 (20,m>=o)인 경우(4.3.2)와 n<19이고 r[n]<m<=r3[n]인 경우(4.3.3)
     #4.5.1 snm[n][m]=snm[0][0]
     #4.5.2 snm[20][m]=0 
     #4.5.3 snm[n][m]=s[m]+snm[n+1][m+1]*p[m]+snm[n+1][m]*(1-p[m])
    #위 연립 방정식을 연립해서 snm[0][0]을 계산하면 됨. reindexing 똑같이해서 snmk도 만듬
    #4.5.1, 4.5.2, 4.5.3로 이루어진 연립방정식을 snmk=A*snmk+b3로 변환.  (A행렬은 동일함)  
    
    b3=np.zeros([kindex])
    
    ##A와 b, b2, b3를 작성.
    for n in range (0,21):
        
        ## (4.3.1)
        #(n,m=r[n])이 가능한 경우인지 체크하기 위해 존재함 (0,0)도 가능하지만 어차피 초기화 안할거라 상관없음.
        if nmtok[n][r[n]]!=0:
            if n!=10:
                if r[n]!=-1:
                    A[nmtok[n][r[n]]][0]=1
                    b[nmtok[n][r[n]]]=cr
                    b2[nmtok[n][r[n]]]=1
            else:
                for m in range(0,r10+1):
                    A[nmtok[n][m]][0]=1
                    b[nmtok[n][m]]=cr                    
                    b2[nmtok[n][m]]=1  
        
        ## (4.3.2) 변경할 것 없음.
        
        ## (4.3.3)
        if n!=20:
            for m in range(r[n]+1,r3[n]+1):
                if m!=10:
                    A[nmtok[n][m]][nmtok[n+1][m+1]]=p[m]
                A[nmtok[n][m]][nmtok[n+1][m]]=1-p[m]
                b[nmtok[n][m]]=cs*s[m]
                b3[nmtok[n][m]]=s[m]
                
    #cmk=inv(I-A)*b
    inv=np.linalg.inv(np.eye(kindex)-A)
    cmk=inv.dot(b)
    rnmk=inv.dot(b2)
    snmk=inv.dot(b3)
    c[i]=cmk[0]
    rn[i]=rnmk[0]
    sn[i]=snmk[0]
    #계산 진행 확인용.
#    if i%10000==0:
#        print(round((i/nN)*100,1),'% 계산완료')

####5. 계산 결과를 통해 최적 전략 출력
##무지성 강화란 main stat이 o강에 도달할 가능성이 존재만 한다면 무조건 강화하는 것을 의미
print('*목표 도달 가능성만 있으면 무지성 강화시 :',round(c[im]/10000,1),'억 메소')
print('*목표 도달 가능성만 있으면 무지성 강화시 초기화 횟수 : ', round(rn[im],2))
print('*목표 도달 가능성만 있으면 무지성 강화시 조각 갯수 : ', round(sn[im],2))
print('*최적전략 사용시 : ',round(c.min()/10000,1),'억 메소')
oi=c.argmin()
print('*최적전략 사용시 초기화 횟수 :', round(rn[oi],2))
print('*최적전략 사용시 조각 갯수 :', round(sn[oi],2))
r10=o-len(N[oi])-1
Ni=np.array(N[oi])
r=np.array([-1 for n in range(21)],dtype=int)
if Ni.shape[0]==0:
    for j in range(10,21):
        r[j]=r10
else:       
    for j in range(10,Ni[0]+1):
        r[j]=r10
    for j in range(0,o-2-r10):
        for k in range(Ni[j]+1,Ni[j+1]+1):
            r[k]=r10+j+1
    for j in range(Ni[o-2-r10]+1,21):
        r[j]=o-1
print('\n*최적전략')
if r[10]!=-1:
    print('10 번 강화시 강화 단계가', r[10], '이하면 초기화')
for i in range(Ni.shape[0]):
    print(Ni[i]+1,'번 강화시 강화 단계가',r[Ni[i]+1],'이면 초기화')