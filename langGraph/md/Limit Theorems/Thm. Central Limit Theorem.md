
>Let $X_1, \; \cdots, X_n \sim \mathsf{iid}(\mu, \; \sigma^2)$
>then $S_n = \sum X_n \sim (n\mu, \; n\sigma^2)$
>So that $\dfrac{S_n - n\mu}{\sigma \sqrt{n}} \sim (0, \; 1)$
>
>Take $n \rightarrow \infty$, then $\dfrac{S_n - n\mu}{\sigma \sqrt{n}} \stackrel {D} \longrightarrow N(0, \; 1)$

매번 iid를 까먹지만, iid란 "독립적이고 동일한 분포"
증명이 좀 빡세다. 무슨 분포인지도 모르는데 어떻게 CDF를 잡아??
근데 요즘 우리에게 MGF가 있다!

## Proof)

If the MGF $M_{X_n}(t)$ of $X_n$ converges pointwise to the MGF $M_X(t)$ of $X$ on some $(-\delta, \; \delta)$,
then $X_n \stackrel {D} \longrightarrow X$

간편하게 $X_1, \; \cdots, \; X_n \sim iid(0, \;1)$이라고 하자

$M(t)$를 $X_i$의 MGF라고 하자
그러면 $M^{(n)}(0) = E(X_i^n)$일거고, #진도추가필요
$M(0) = 1$, 
$M^\prime(0) = E(X_i) = 0$,
$M^{\prime\prime} (0) = E(X_i^2) = Var(X_i) + E(X_i)^2 = 1$이라고 할 수 있을거다

Let $Y_n = \dfrac {1}{\sqrt{n}} (X_1 + \cdots + X_n)$
일단 $Y_n$을 분산이 1이 되도록 만든 모습. 표준화의 역할.
Then $M_{Y_n}(t) = E(e^{tY_n}) = E(e^{\frac{t}{\sqrt{n}}(X_1 + \cdots + X_n)})$이고,
우측 식을 풀어준 다음에, 
$X_n$들이 independent하니까 $E(e^{\frac{t}{\sqrt{n}}X_1})$의 곱들로 완성이 될거고,
이들은 모두 같으니, 좀 편하게 표현해서 $M_{Y_n}(t) = M(\dfrac{t}{\sqrt{n}})^n$라고 하자

양쪽에 ln 씌우고, $w = \dfrac{1}{\sqrt{n}}$하면, $n \rightarrow \infty$할 때 $w \rightarrow 0^+$겠지
우항에 올 $lim _{w \rightarrow 0^+}\dfrac{\mathsf{ln} M(wt)}{w^2}$에 $w$에 대해서 로피탈을 하면?
뭐가 나오고, 거기에 분모분자에 0을 넣을 수 있는 부분은 넣고,
또 로피탈을 하면? $\mathsf{ln} M_{Y_n}(t) = \dfrac{t^2}{2} \Longrightarrow lim_{n \rightarrow \infty} M_{Y_n}(t) = e^{\frac{t^2}{2}}$

$Z \sim N(0, \; 1)$의 MGF로 수렴한 모습!! $Y_n \stackrel {D} \longrightarrow Z$
Degree of freedom이 없다! $n$하고 상관이 없어!
그 대상이 독립적인거 무수히 더한거라면 정규분포를 쓰면 된다!

$\sum X_k$는 normal distribution에 근접하다!