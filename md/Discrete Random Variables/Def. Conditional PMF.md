>If $x$, $y$ are random variables on the sample space $\Omega$,
>we define
>$$p(x| y) = P(\{X = x\} | \{Y = y\}) = \dfrac{P(x, \;y)}{P_Y(y)}$$
>which is called **conditional PMF**

**$X$의 PMF로** $y$가 정해진 상태에서 $P(X=x|Y=y) = p(x|y)$로 [[Def. Conditioning|조건부확률]]을 [[Def. Discrete Random Variable & PMF|PMF]]로 쓰는거지!

$$\sum _x P(x | y) = \dfrac{\sum _x P(x, \;y)}{P_Y(y)}$$
하면 1 나오니까 일단 PMF는 맞다!
당연히 $\sum _y P(y | x)$도 1이겠지!

평균은 $E(X|y) = \sum x P(x|y)$
분산은 $Var(X|y) = E(X^2 | y) - E(X | y)^2$
LoTuS는 $E(g(X) | y) = \sum g(x) \cdot p(x|y)$일거야
