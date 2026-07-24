>[[Def. Discrete Random Variable & PMF|이산확률변수]]에서, $X$의 분산은
>$E[(X - \mu_X)^2] = Var(X)$로 정의된다
>$\mu_X$는 표본에서 측정된 평균값을 의미

미분가능한 양수를 만들기 위해
그냥 그대로도 아닌, 절댓값도 아닌, 제곱으로 표현한거지

근데 이러면 제곱 되어 있으니까 단위가 $\%^2$이란 말이지
그래서 단위를 맞추기 위해
>표준편차를 $\sigma_X = \sqrt{Var(X)}$로 정의.

그렇지만 아직 식이 너무 보기가 안 좋다.

$$\begin{alignedat}{1}
Var(X) =& E[(X - \mu_X)^2] \\
=& E((X^2 - 2 \mu X + \mu^2))
\end{alignedat}$$
여기서 $E(aX + b)$를 [[Thm. LoTuS for PMF|LoTuS]]에 넣으면
쉽게 $aE(X) + b$가 되는걸 알 수 있으니
이를 이용하면....
$$ = E(X^2) - 2\mu E(X) + \mu^2$$
$E(X)$를 $\mu$로 본다면...
$$Var(X) = E(X^2) - E(X)^2$$
우리가 흔히 아는 그 식이 완성된다!!

# # $Var(aX + b)$

[[Thm. LoTuS for PMF|LoTuS에 의해]]
$$\begin{alignedat}{1}
Var(aX + b) =& E((aX + b) - (a \mu_X + b)) \\
=&E([a(x-\mu_X)]^2)
\end{alignedat}
$$
[[Def. 평균. 이산확률변수에서의#$E(aX + b)$|평균의 활용에 의해]] $a^2$을 앞으로 뺄 수 있지. 즉,
$$\begin{alignedat}{1}
&Var(aX + b) = a^2 Var(X) \\
&\sigma_{aX+b} = |a| \sigma_X
\end{alignedat}$$
