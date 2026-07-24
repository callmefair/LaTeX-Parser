>Let $A$ and $B$ be [[Def. Discrete Random Variable & PMF|Discrete RV]], then
>$$P (A | B) = \frac {P(A \cap B)}{P(B)}$$

이제 좀 조건부확률 얘기를 해볼 시간

>If $x$ is a discrete random variable in $X$,
>$$P(x | A) = \frac {P(\{X = x\} \cap A)} {P(A)}$$

근데 이게 확률변수 값 하나에서도 정의가 되네!!

여러 $x$에서 [[Def. Random Variable|이 함수를 생각하면]]
이 $\{X = x\} \cap A$들은 disjoint해. 아직 증명된건 아니지만...
링크에서 보다시피 $P(\{X =  x\})$는 $\{\omega \in \Omega \;|\; X (\omega) = x\}$로 볼 수 있어

그러면
$$P(A) = \sum _{x \in R_X} P(\{X = x\} \cap A)$$
$R_X$는 말했다시피 [[Def. Random Variable|여기서 본 함수의]] range고,
$X$가 가질 수 있는 값과 $A$의 교집합이 곧 $P(A)$가 되는거지.
모든 $x$에서의 $A$와의 교집합의 경우를 다 합치면 당연히 $A$의 확률이 나올테니.
$x$가 $A$ 안에 있든, 밖에 있든 다 합치면 ㅇㅇ

$X$는 확률변수니까 $x \in X$가 틀린 표현임을 염두에 두자.

여담으로 이게 지금 확률이 합으로 표현됐잖아?
그럼 어차피 P들을 다 합친거니까 저 중에 음수가 되는 것도 상상해볼 수 있지 않을까?
측도론적으로 생각하면, 나중에 음인 확률이 나올 수도 있나봐

아무튼 위의 식으로 인해 $\sum _{x \in R_X} P(x | A) = 1$이다
>For each event $A$ (with $P(A) > 0$), 
>$P(x|A)$ is a PMF conditioned by $A$.

condition으로 표현된 PMF가 완성이 되는 모습!

# Conditioning의 평균

$P(x | A)$를 $P(X|A)$의 PMF인 $p(x)$로 생각할 수 있을거고,
PMF랑 [[Def. 평균. 이산확률변수에서의|평균 식]]생각하면
$$ E(X | A) = \sum _{x \in R_X} x \cdot P(x | A)$$
로 생각하면 되겠지