>$E(X | y) = E(X | \{Y = y\})$
>is called **conditional expectation**.

[[Def. Conditional PMF|Conditional PMF]]에다가 [[Def. 평균. 이산확률변수에서의|평균]] 씌운거!!

[[Obj. Binomial Random Variable]]가 사실 여기서 유도할 수 있음을 알 수 있어!
$$
E(X) = \sum _x x P_X(x) = \sum _x x \sum _y P(x, \; y)$$
여기서 [[Def. Conditional PMF|Conditional PMF]] 쓰면
$$= \sum _x x \sum _y P_Y(y) \cdot p(x| y)$$
$x$, $y$ 시그마 자리 바꾸면?
$$= \sum _y P_Y(y) \sum _x x \cdot  p(x| y)$$
이 뒤의 시그마가 $E(X|y)$네!
>$$\therefore E(X) = \sum _y P_Y(y) \cdot E(X | y)$$

이게 이제 $y$가 [[Thm. Total Expectation Law|Total Expectation Law]]의 $B_k$ 역할을 하는 느낌!