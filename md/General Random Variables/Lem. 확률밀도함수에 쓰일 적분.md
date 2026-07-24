>$\int _{-\infty} ^\infty e^{-x^2} dx$는 존재한다. 

근데 미적분학의 기본정리로 구할 수 없어
그래서 극좌표로 구한다고 하네?

위의 적분을 $I$라고 한다면,
$$\begin{alignedat}{1}
I^2 =& \int _0 ^\infty e^{-x^2} dx \int _0 ^\infty e^{-y^2} \; dy \\
=&\int _0 ^\infty  \int _0 ^\infty e^{-(x^2+y^2)} dx \; dy \\
=&\int _0 ^\infty  \int _0 ^\infty e^{-(x^2+y^2)} dx \; dy \\
\end{alignedat}$$
[[테크닉5]]
이야... 제곱해서 극좌표로 구한다니 진짜 상상도 못했네....
여기서 $x = rcos\theta$, $y= rsin\theta$로 두면 $dxdy = r \; drd\theta$
$$I^2 =\int _0 ^{\pi / 2} \int _0 ^\infty e^{-r^2} rdr \; d\theta = \dfrac {\pi} {4}$$
물론 우리가 구하는건 이게 아니라,
$$\therefore\int _{-\infty} ^\infty e^{-x^2} dx = 2I = \sqrt{\pi}$$

그럼 $\int _{-\infty} ^\infty e^{-t^2 / 2} \; dt$는 어떻게 구해?
$x = t / \sqrt{2}$로 치환하면? 
$$\int _{-\infty} ^\infty e^{-t^2 / 2} \; dt = \sqrt{2\pi}$$