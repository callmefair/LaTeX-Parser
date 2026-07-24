#convergence 

>Let $X_n$ be rv with CDF $F_{X_n}(x)$
>Let $X$ be rv with CDF $F_{X}(x)$
>If $lim_{n \rightarrow \infty} F_{X_n}(x) = F(x)$ for all $x$ at which $F$ is continuous,
>
>we say $\{X_n\}$ **converge to $X$ in distribution**
>$$X_n \stackrel {D} \longrightarrow X$$
>if $F_{X_n}(x)$ converges to $F_X(x)$ which is CDF of $X$

근데 실제로는 수렴하는 곳이 정해져있는데...

>Let $\{X_n\}$ be a sequence of rvs
>whose CDF is $F_{X_n}(x)$
>Let $\Phi (x) = \int _{-\infty}^x \dfrac{1}{\sqrt{2\pi}} e^{-t^2 /2} dx$
>
>If $lim_{n \rightarrow \infty} F_{X_n}(x) = \Phi (x)$,
>then for $X_n$ with large n, 
>we can use the table of $Z \sim N(0, \;1)$
>
>Which is denoted by $X_n \stackrel {D} \longrightarrow N(0, \; 1)$

겉모양만 보고 판단. 내용은 보지 않는다!
어떤 $X_n$이든 많아지면 그냥 정규분포함수로 쓸 수 있다!
분포적인 수렴은 [[Def. Convergence in Probability|해석학적인 수렴]]의 티끌만도 찾아볼 수가 없지...

## 분포 수렴을 아니꼽게 보게 되는 점 1

$X_n \sim N(0, \; n) \Rightarrow \dfrac {X_n}{\sqrt{n}} \sim N(0, \; 1)$
$Y_n \sim N(0, \; \dfrac{1}{n}) \Rightarrow \sqrt{n} {Y_n} \sim N(0, \; 1)$
이 둘은 [[Def. 분산과 표준편차. 이산확률변수에서의#$Var(aX + b)$|분산의 식을 이용해서]] $N(0, \; 1)$으로 만들 수 있어

### # X_n

Let $P(X_n \leq x) = F_{X_n}(x)$ be the CDF of $X_n$
그러면 $P$ 안의 식을 $\sqrt{n}$으로 나누면 $\Phi (\dfrac{x}{\sqrt{n}})$이야
이거 $n \rightarrow \infty$하면? $x$가 뭐든 $\Phi (0)$ 나오고, 이 수치는 정의에 의해서 $1/2$겠지

그러니 $P(X_n \leq x)=F_{X_n}(x)$는 $n$ 커지면 무조건 $1/2$로 간다!!
이건 전혀 CDF의 정의에 맞지 않는다!
**$X_n$은 어디에도 converge하지 않는다!**

사실 이건 분산이 발산할 때부터 싹수가 보였어

### # Y_n

$P(Y_n \leq y)$도 양쪽을 $\sqrt{n}$을 곱하면 $\Phi(\sqrt{n} y)$
이것이 $n$을 무한대로 보내면 
$$P(Y_n \leq y)=\begin{cases} 0 & \mathsf{if\;} y < 0 \\ 1/2 & \mathsf{if \;} y = 0 & \\1 & \mathsf{if\;}y>0 \end{cases}$$
[[Def. Continuous Random Variable & CDF|CDF의 진짜 정의상]] monotone increasing해야 하는데,
이게 right continuous이기만 하면 되거든! #확인필요
그래서 왼쪽으로부터의 점프는 되는데, 
이렇게 $y = 0$에서 오른쪽 점프까지 해버리면 CDF라고 볼 수가 없다!

얘도 분산이 사실 0으로 가니 적분 1 만드려고 0 근처에서 겁나 커지는 형태지

**아무튼 얘네 둘은 분포상 정규분포함수로 갈 수 있다고 하지만, 엉터리 확률변수다!!**

#### 그나마 분포 수렴을 더 보여준다면,

Let $Y$ has a PMF $g(y) = \begin{cases} 1 & \mathsf{if\;} y = 0 \\ 0 & \mathsf{else} \end{cases}$
이제 PMF를 CDF로 생각해볼 수 있나보다. $Y$를 CDF로 생각해본다면 #확인필요 
$$G(y) = \begin{cases} 1 & \mathsf{if\;} y \geq 0 \\ 0 & \mathsf{if \;} y<0 \end{cases}$$
$G$는 $\mathbf{R} \backslash \{0\}$에서 continuous하니, 
pointwise convergence로 $F_{Y_n} \rightarrow G$ on $\mathbf{R} \backslash \{0\}$라고 할 수 있으니 #개념추가필요
$Y$가 사실상 $\mathbf{R} \backslash \{0\}$에서 0이니....
$$Y_n \stackrel {D} \longrightarrow 0$$
이런 충격적인 결과가 나온다.
그나마 $Y_n$이라서 이 정도지, 1로 가지도 못하는 $X_n$은 가망도 없다!

## 분포 수렴을 아니꼽게 보게 되는 점 2

$Z \sim N(0, \; 1)$, $X_n = Z$, $Y_n = -Z$

$$\begin{alignedat}{1}
F_{Y_n}(y) = P(Y_n \leq y) &= P(-Z \leq y) \\
&= P(Z \geq -y) \\ 
&= 1 - \Phi(-y) = \Phi(y) = F_{X_n}(y)
\end{alignedat}$$
아예 부호가 반대인데 분포가 같다고 하네...
분포 $P(Z \geq -y)$만 봐선 안에 있는 확률변수 $Y_n = -Z$가 뭐가 있는지 알 길이 없다!

## 대신 극한으로 간 PMF를 누적분포함수로 보는 역할

Let $Y_n$ be a discrete uniform rv on $\{1, \; \cdots, \; n\}$
Then $P_{Y_n}(y) = 1/n$ and let $X_n = Y_n / n$

그러면 PMF는 $P_{X_n} (x) = P(X_n = x) = 1/n$겠지
지금 $x$가 어디에서 정의되어 있는지 계속 생각해야 해

그러면 CDF $F_{X_n}(x)$는 $x \leq 0$이면 0, $x \geq 1$이면 1
$0 < x < 1$이라면?
$$ \sum _{k=1} ^{[nx]} P(X_n = \dfrac{k}{n}) = \dfrac {[nx]}{n}$$
그러면 $F_{X_n}(x)=\dfrac{[nx]}{n}$이고, $\dfrac{nx -1}{n} < F_{X_n}(x) \leq \dfrac{nx}{n}$이니까 $x-\dfrac{1}{n} < F_{X_n}(x) \leq x$
$$\lim_{n\rightarrow \infty}F_{X_n}(x) = \begin{cases} 0 & \mathsf{if\;} x \leq 0 \\ x & \mathsf{if \;} 0 < x < 1 & \\1 & \mathsf{if\;}x\geq1 \end{cases}$$
lim 맛깔나게 보내면 uniform\[0, 1]과 같은 분포가 나온다!!
$$X_n \stackrel {D} \longrightarrow X \sim \mathsf{uniform}[0,\;1]$$
아무리 PMF를 극한으로 본들, 적분 때려봤자 0이고, lim 때려봤자 암것도 안나오는데,
Converge in Distribution으로 누적분포함수로 볼 수 있는 건덕지는 생기겠지!

