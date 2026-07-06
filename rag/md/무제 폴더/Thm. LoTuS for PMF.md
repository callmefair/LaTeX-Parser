Lotus: Law of the Unconscious Statistician

>If $X$ is a [[Def. Discrete Random Variable & PMF|discrete RV]] and $Y=g(X)$
>and p(x) is a PMF of $X$,
>Then $E(Y) = \sum _{x \in R_X} g(x) p(x)$

이게 곧 [[Def. 평균. 이산확률변수에서의|평균]] $E(Y)$를 구하는데 $Y$의 PMF가 필요없다는 소리!

$E(X^2) = \sum x^2p(x)$
$E(e^X) = \sum e^x p(x)$

# Y의 PMF 따윈 필요 없다

Inverse image로 이렇게 잡아보자.
$$g^{-1}(y) = g^{-1}(\{y\}) = \{x \in R_X \;|\; g(x) = y \}$$
$R_X$라는건 [[Def. Random Variable|여기서 나오는 X 함수에서]] range의 역할.
확률변수 $X$가 가질 수 있는 모든 값들의 집합

아무튼 이제 진짜 $Y$가 PMF가 없다는걸 드러내고 싶은데...
$P_Y(y)$가 $Y$의 PMF라고 하자.

$$\begin{alignedat}{1}
P_Y(y) =& P(Y=y) = P(g(X) = y) \\
=& P(\{X = x_1\} \cup \{X = x_2\} \cup \cdots)
\end{alignedat}$$
아직 확률변수 $X$ 함수를 제대로 알고 있는건 아니지만,
저 $\{X = x_1\}$ 사건과 $\{X = x_2\}$ 사건은 동시에 일어날 수 없으며,
disjoint하다고 보는게 타당해.

그래서 다음과 같이 sum을 만들 수 있지.
$$
P_Y(y) = \sum _{x \in g^{-1}(y)} p(x) \\
$$
여기서 [[Def. 평균. 이산확률변수에서의|E(Y)를 때려박으면?]]
$$E(Y) = \sum _{y \in R_Y} y \times P_Y(y) = \sum _{y \in R_Y} y \sum _{x \in g^{-1}(y)} p(x) $$
이제 $y$를 오른쪽 시그마에 집어넣고,
$y$를 $g(x)$로 바꾸고,
시그마 두 개의 $y \in R_Y$랑 $x \in g^{-1}(y)$는 그냥
시그마 $x \in R_X$로 합친다면,

*이게 헷갈릴 수 있지만 $y \in R_Y$마다 $x \in g^{-1}(y)$하자는거를
그냥 어차피 식 안의 모든게 $x$로 표현되는거 
"모든 x에 대하여" 같은 느낌으로 표현해도 아무렴 어떠냐는 마인드*

결국은
$$ E(Y) = E(g(X)) = \sum g(x) P_X(x)$$
**결국 $Y$의 PMF라곤 찾아볼 수 없는 식이 완성된다!**


