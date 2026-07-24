>$CoV(X, \; Y)$ is defined by
>$$ \begin{alignedat}{1}
CoV(X, \; Y) =& E((X - \mu_X)(Y-\mu_Y))
\end{alignedat}$$

이 식을 [[Def. 평균. 이산확률변수에서의#$E(aX + b)$|또 평균 풀어내면]], 맨 앞에 $E(XY)$랑
3개의 $E(X)E(Y)$ 식이 더하고 빠져서 남는건
$$CoV(X, \;Y) = E(XY) - E(X)E(Y)$$
간혹 $E(X)E(Y)$ 대신 $\mu_X \mu_Y$를 쓰기도 하는거 같고...

여기서 $X$랑 $Y$가 independent하면, [[Thm. 독립과 평균, 분산#평균|평균 식에 의해]]
$E(XY) = E(X)E(Y)$니까 $CoV(X, \; Y) = 0$

>$$\rho = \dfrac{CoV(X, \; Y)}{\sigma_X \sigma_Y}$$
>is called a **correlation coefficient** of $X$ and $Y$

이제 [[Def. 분산과 표준편차. 이산확률변수에서의|분산(표준편차) 개념]]까지 가져오면 상관계수를 정의할 수 있어!

# CoV(X+a, Y+b)

$$CoV(X+a, \;Y+b) = E[(X+a)(Y+b)] - E(X+a)E(Y+b)$$
역시 $E[(X+a)(Y+b)]$ 식 풀어내면 뒤에꺼가 많이 사라지고,
남는건
$$=E(XY) - E(X)E(Y)=CoV(X, \;Y)$$
분산의 성질을 엿볼 수 있는 부분이지!!

