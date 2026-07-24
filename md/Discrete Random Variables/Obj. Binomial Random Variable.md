>$X \sim B(n, \; p)$ denotes the # of success
>n번의 독립적인 [[Obj. Bernoulli Random Variable|베르누이 시행에서!]]
>where $n$ is # of trials, and $p$ is probability of success. 

[[Def. Discrete Random Variable & PMF|이산확률변수]]의 일종
>$X \sim B(n, \; P)$면
>$$P(X = k) =  \begin{equation}
\begin{pmatrix}
n \\
k
\end{pmatrix}
\end{equation} p^k (1-p)^{n-k}$$
>당연히 $k = 0$부터 $n$까지인 정수일거고...

다 더해서 1이 되는걸 확인해볼까?
$$\sum _{k=0} ^n P(X = k) = [p + (1 - p)] ^n = 1$$
이게 이렇게 되는건 솔직히 직관적으로 그 숫자 삼각형을 떠올리면 되겠지....

# # 평균

[[Def. 평균. 이산확률변수에서의|평균 식에 의해]]
$\begin{equation} E(X) = \sum _{x=0} ^n x \times \begin{pmatrix} n \\ x \end{pmatrix} p^x q^{n-x}\end{equation}$
1\. 이러니 0은 제외해도 되니 $\sum _{x=1}$로 바꿔줌.

2\. $\begin{equation} k \begin{pmatrix} n \\ k \end{pmatrix} = n\begin{pmatrix} n-1 \\ k-1 \end{pmatrix} \end{equation}$인걸 이용하면
시그마 식 앞의 $x \begin{pmatrix} n \\ x \end{pmatrix}$를 $n\begin{pmatrix} n-1 \\ x-1 \end{pmatrix}$로 바꿔줄 수 있고.

3\. 그 상태에서 $n$과 $p$를 하나씩 빼고,
$q$의 지수의 $n-x$를 $(n-1) - (x-1)$로 바꿔주면?
$\begin{equation} E(X) = np \sum _{x=1} ^n \begin{pmatrix} n-1 \\ x-1 \end{pmatrix} p^{x-1} q^{(n-1)-(x-1)}\end{equation}$

4\. 이제 1부터 $n$ 까지였던 시그마를 0부터 $n-1$ 까지로 바꿔주고,
$x-1 \rightarrow x$로 해주면
뒤의 식은 Binomial Sum이 되어 1로 사라짐

$$\therefore E(X) = np$$

# # 분산

[[Def. 분산과 표준편차. 이산확률변수에서의|분산 식]]을 이용하면...
$E(X)^2$는 위의 평균처럼 노가다 하면 $n(n-1)p^2 + np$
$E(X)=np$니까
$$\begin{alignedat}{1}
Var(X) =& n(n-1)p^2 + np - n^2p^2 = np - np^2 = np (1-p) \\
=& npq
\end{alignedat}$$

# Joint PMF 관점

Binomial은 $n$번의 독립적인 Bernoulli 시행에서의 성공 횟수니까
[[Obj. Bernoulli Random Variable|베르누이 시행에서]] $k$번째에서 성공하는걸 생각해보면...
$$ E(X_k) = p \times 1 + (1 - p) \times 0 = p $$
뭐 말할 것도 없이 어느 $k$에서든 이러겠지.

근데 말했다시피 독립적으로 $X \sim B(n, \; p)$ with $X = X_1 + \ldots + X_n$라고 한다면
[[Thm. E(X+Y) = E(X) + E(Y)|Joint PMF의 정리]]를 이용한다면
$$E(X) = E(X_1) + \ldots + E(X_n) = np$$
우리가 위에서 본 평균이 나온다!

# 총 k번의 시행에 X가 j번 시행될 확률 

>Let $X \sim B(m, \; p)$ and $Y \sim B(n, \; p)$ are independent,
>Find $P(X = j \;|\; X + Y = k)$

이러면 
$0 \leq j \leq m$, 
$j \leq k \leq j + n$이겠지?

[[Def. Conditioning|조건부확률]]이랑 우리가 아는 교집합으로 된 간단한 독립 정의 사용하면,
$$P(X = j \;|\; X + Y = k) = \dfrac{P(X=j) \cdot P(Y = k -j)}{P(X+Y = k)}$$
그리고 independent 하니까
분모에서 $X+Y \sim B(m+n, \; p)$이라고 할 수 있겠지?
<참고로 이것도 증명이 필요하긴 해서 gemini에 얘기한거 봐봐>
Binomial 정의 사용하면, 
$$ = \dfrac{\begin{pmatrix}
m \\ j \end{pmatrix}
 p^j (1-p)^{m-j} \cdot
 \begin{pmatrix}
n \\ k-j \end{pmatrix}
 p^{k-j} (1-p)^{n-(k-j)}}{\begin{pmatrix}
m+n \\ k \end{pmatrix}
 p^k (1-p)^{(m+n)-k}} 
 $$
제곱 부분 다 합치면, 바로
$$P(X = j \;|\; X + Y = k) = \dfrac{\begin{pmatrix}
m \\ j \end{pmatrix}
 \cdot
 \begin{pmatrix}
n \\ k-j \end{pmatrix}}
{\begin{pmatrix}
m+n \\ k \end{pmatrix}}
 $$
근데 생각해보면 애초에 $P(X = j \;|\; X + Y = k)$ 말하는거 자체가 [[Obj. Hypergeometric Random Variable|Hypergeometric RV]]다!
지금 형태 보면 $n$ 자리에 $m+n$으로 끼워놓은 모습!!