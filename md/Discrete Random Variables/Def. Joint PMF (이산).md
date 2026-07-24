>$$p(x, \; y) = P(X = x \; \mathsf{and} \; Y=y)$$
>such that
>$$\sum _{x, \; y} p(x, \; y) = 1 \; \mathsf{and} \; 0 \leq p(x, \;y)\leq 1$$
>is called the **Joint PMF** of $X$ and $Y$

사실 그냥 2차원으로 정의된 확률과 [[Def. Discrete Random Variable & PMF|PMF]] 아닐까?
 
# Marginal PMF

이 경우에 $X$에서의 [[Def. Discrete Random Variable & PMF|PMF]]는
$$P_X(x) = P(X = x) = \sum_{y} p(x, \; y)$$
는 $X$가 $x$로 정해져있는 셈이니, $y$만 생각하면 되니
**marginal PMF**라고 한다.

# LoTuS

>Let $X, \; Y$ be random variables in some $\Omega$.
>Then we define 
>$$ E(f(X, \; Y)) = \sum _{x, \; y} f(x, \; y) \cdot p(x, \; y)$$

이것도 [[Thm. LoTuS for PMF|LoTuS]] 맥여보는 모습
하지만 이게 성립하기 위해선 $E(\vert f(X) \vert) = \sum |f(x)| p(x) < \infty$을 가정해야 한대.
물론 이러지 않는 것까지 생각하면 별로 반례 존재하지도 않는 해석학의 영역에 들어오지

#### 지피티

사실 이 조건은 1차원 PMF에서도 필요한 조건이다.
근데 1차원에선 기댓값이 존재하지 않는다 정도로 얘기하면 되는데,
2차원에선 합의 순서 교환 문제가 생겨.
고등미적분 이야기인데... 잠시 remind하자

$$\sum _{x, \; y} f(x, \; y) \cdot p(x, \; y)$$
이게 잘 정의되려면 절대수렴이 되어야 해.
$$E(\vert f(X, \; Y) \vert) = \sum |f(x, \; y) \cdot p(x, \; y)| < \infty$$
그리고 그 절대수렴이란건....
$$\sum _x \sum _y f(x, \;y) \cdot p(x, \; y) = \sum _y \sum _x f(x, \;y) \cdot p(x, \; y)$$
이렇게 절대수렴이 안되지만 부분합은 수렴하는걸 조건부 수렴이라고 하는데....
이 경우에는 합의 순서를 바꾸면 결과가 달라지는 그 상황이 되는거지!

이런 현상 때문에 2차원에서 강조하셨나봐
