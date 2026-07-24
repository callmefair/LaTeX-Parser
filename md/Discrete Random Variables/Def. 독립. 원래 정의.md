# 원래 정의

>Let $X$, $Y$ be random variables on the same sample space $\Omega$

그럼 [[Def. Discrete Random Variable & PMF|이산]], 연속 상관없이 독립은 이렇게 정의돼.
Measurable의 이야기야

>$$P(\{X \leq x\} \cap \{Y \leq y\} ) = P(X \leq x) \cdot P(Y \leq y)$$
>for all $x, \; y \in \mathbb{R}$

무언가... 수치적으로 정의가 되나봐?
되게 의외의 정의네.

# 확률론 전용 정의

근데 우리 확률론에서의 정의는? 측도론의 정리와 달라
>For every $G, \; E \subset \mathbb{R}$
>$$ P(X \in  G \; \mathsf{and} \; Y\in E) = P(X \in G) \cdot P(Y \in E)$$

위에꺼보다 더 강한 정의지
$G, \; E$를 위에처럼 정의하면 그만이니까.

이런 식으로 정의하면,
모든 measurable event, 모든 확률 event 다 정의 가능하대
