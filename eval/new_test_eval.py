from eval.metrics.rest_metric import ff_metric, cp_metric, cr_metric
from eval.metrics.geval_metric import se_metric, ar_metric, ne_metric

from deepeval.test_case import LLMTestCase
from deepeval import evaluate

def scoring(question, reference, candidate, metric, retrieval_chunk):
    scores = []
    for name, expected, text in candidate:
        tcargs = {
            "input": question,
            "actual_output": text
        }
        if reference:
            tcargs["expected_output"] = [reference]
        if retrieval_chunk:
            tcargs["retrieval_context"] = [retrieval_chunk]
        
        tc = LLMTestCase(**tcargs)
        metric.measure(tc)
        
        score = metric.score
        scores.append(score)
        diff = score - expected
        
        print(metric.name)
        print(f"{name}: {score:.2f}점 (기대 {expected:.2f}) -> {diff:+.2f}점 차이")
        print(metric.reason)
        print("---")

    if len(scores) >= 3:
        print(f"정상 {scores[0]:.2f} / 절반 {scores[1]:.2f} / 망함 {scores[2]:.2f} "
            f"| 판별력 {scores[0] - scores[2]:.2f}")


if __name__ == "__main__":
    """
    QUESTION12 = "Central Limit Theorem은 무엇을 의미하나요?"
    REFERENCE12 = (r"평균 $\mu$, 유한한 분산 $\sigma^2$을 갖는 iid 확률변수들의 합 $S_n$을 "
             r"표준화한 $\frac{S_n - n\mu}{\sigma\sqrt{n}}$은, 원래 분포의 형태와 무관하게 "
             r"$n \to \infty$일 때 표준정규분포 $N(0,1)$로 분포 수렴한다.")
    CANDIDATES1 = [
        ("정상", 1.0, r"중앙한계정리(Central Limit Theorem)는 i.i.d.(독립동일분포)를 따르는 확률변수들의 합 $S_n$을 표준화한 통계량 $\frac{S_n - n\mu}{\sigma\sqrt{n}}$이 표본 크기 $n$이 무한히 커짐에 따라 원래 분포의 형태와 상관없이 표준정규분포 $N(0, 1)$로 수렴한다는 정리를 의미합니다."),
        ("절반", 0.5, r"중앙한계정리는 모집단에서 표본을 추출할 때 표본평균의 분포를 설명하는 통계학의 핵심 정리입니다. 표본 크기가 보통 30 이상이면 적용할 수 있으며, 신뢰구간 형성이나 가설검정에서 유의확률을 구할 때 많이 활용됩니다. 한편 독립동일분포(i.i.d.)를 따르는 확률변수의 합 $S_n$을 표준화한 $\frac{S_n - n\mu}{\sigma\sqrt{n}}$은 $n$이 커질수록 표준정규분포 $N(0, 1)$로 수렴하게 되는데, 이와 유사한 개념으로는 표본평균이 모평균에 수렴한다는 대수의 법칙(Law of Large Numbers)도 존재합니다."),
        ("망함", 0.0, r"중앙한계정리(CLT)는 데이터의 중앙값(Median)과 최빈값(Mode)이 중심경향성을 나타낼 때 표준편차 범위 내에 데이터의 몇 퍼센트가 들어오는지를 측정하는 정리입니다. 주로 데이터 시각화 시 히스토그램의 중심축을 정하기 위해 사용하며, 데이터 수가 늘어날수록 분포가 균등분포(Uniform Distribution) 형태에 가깝게 평평해진다는 것을 나타냅니다."),
    ]

    scoring(QUESTION12, REFERENCE12, CANDIDATES1, ar_metric, None)

    CANDIDATES2 = [
        ("정상", 1.0, r"독립동일분포(i.i.d.)를 따르는 확률변수들의 합을 $S_n$이라 할 때, 이를 표준화한 식인 $\frac{S_n - n\mu}{\sigma\sqrt{n}}$은 표본의 개수 $n$이 무한대로 증가함에 따라 원래 확률변수가 어떤 개별 분포를 가지든 상관없이 표준정규분포 $N(0, 1)$로 수렴한다는 것을 의미합니다."),
        ("절반", 0.5, r"확률변수들의 합 $S_n$을 표준화한 $\frac{S_n - n\mu}{\sigma\sqrt{n}}$은 $n$이 무한대로 갈 때 표준정규분포 $N(0, 1)$로 수렴합니다. 단, 이 정리년 원래 확률변수들이 정규분포를 따를 때만 성립합니다."),
        ("망함", 0.0, r"중앙한계정리는 머신러닝 모델의 과적합(Overfitting)을 방지하기 위해 경사하강법에서 학습률(Learning Rate)을 제어할 때 핵심이 되는 통계적 규칙을 의미합니다."),
    ]

    scoring(QUESTION12, REFERENCE12, CANDIDATES2, ar_metric, None)

    '''
    정상 0.80 / 절반 0.70 / 망함 0.10 | 판별력 0.70
    정상 0.90 / 절반 0.30 / 망함 0.00 | 판별력 0.90
    '''
    
    QUESTION3 = "Markov Inequality는 왜 이런 의미를 가질까용?"
    CANDIDATES3 = [
        ("정상", 1.0, r"마르코프 부등식(Markov's Inequality)은 음이 아닌 확률변수 $X$에 대해 $X \ge a$일 확률의 상한을 나타내는 정리입니다.원문 문서의 설명에 따르면, $X$에 대해 알 수 있는 정보가 극히 제한적이고 평균 값 $E(X)$만 알고 있을 때 유용하게 활용할 수 있어요. 전체 기댓값 정리(Total Expectation Law)를 활용해 부등식을 유도하면 $P(X \ge a) \le \frac{E(X)}{a}$라는 관계가 도출됩니다.다만 정보가 거의 없을 때 사용하는 완화된 상한선이다 보니, 균등분포처럼 구체적인 확률분포를 이미 알고 있는 경우에는 다소 당연하거나 범위가 넓은 결과(예: 확률이 1 이하라는 식의 결과)가 나올 수 있다는 점도 함께 참고하시면 좋습니다."),
        ("절반", 0.5, r"마르코프 부등식은 $X$가 음이 아닌 확률변수일 때 $P(X \ge a) \le \frac{E(X)}{a}$가 성립한다는 의미입니다.기댓값 정리에서 일부분을 떼어내 부등식을 완성하는 방식인데요, $X$에 대해 정말 아무 정보가 없으면 이거 쓰는 겁니다. uniform[0, 4] 같은 분포 정보가 이미 있는데 쓰면 확률이 1보다 작거나 같다는 너무 도움 되는(?) 결과가 나오기도 해요. 사실 체비쇼프 부등식 같은 스승 theorem 내용을 베끼고 이름 붙인 느낌이 성립 배경에 들어있습니다."),
        ("망함", 0.0, r"$X$에 대해 정말 아무 정보가 없을 때 쓰는 정리임. $A = {X \ge a}$로 잡고 Total Expectation Law에서 일부만 떼어내면 $E(X) \ge P(A) \cdot E(X\vert{}A)$가 됨.정보가 있는데 쓰면 Uniform[0,4]일 때 $P(X \ge 2) \le 1$ 나와서 확률이 1보다 작거나 같다는 소리나 하게 됨 ㅋㅋㅋ 그냥 스승 Chebyshev Inequality 베끼고 이름 붙인 거라 보면 됨."),
    ]

    scoring(QUESTION3, None, CANDIDATES3, ne_metric, None)

    QUESTION4 = "LoTuS에서 왜 Y의 PMF가 필요없게 되는지가 궁금하다. 얼른 말하도록."
    CANDIDATES4 = [
        ("정상", 1.0, r"LoTuS(무의식적 통계학자의 정리)에서 $Y$의 PMF가 필요 없는 이유는, $Y = g(X)$의 기댓값을 구할 때 $X$의 PMF인 $P_X(x)$와 함수 $g(x)$만으로 식을 완전히 전환할 수 있기 때문입니다.원문 문서의 증명 과정을 살펴보면, $Y=y$가 되는 $X$의 역상(Inverse image) 집합 $g^{-1}(y)$을 이용하여 $Y$의 PMF인 $P_Y(y)$를 $X$의 확률들의 합으로 표현합니다. 이 식을 기댓값 정의 $E(Y) = \sum y P_Y(y)$에 대입한 뒤 시그마를 합치고 변수를 $x$ 기준으로 정리하면, 결과적으로 $E(Y) = \sum g(x) P_X(x)$ 형태가 완성됩니다.따라서 $Y$ 자체의 확률분포(PMF)를 직접 구하지 않고도 $X$의 정보만으로 $Y$의 평균을 쉽게 계산할 수 있게 됩니다."),
        ("절반", 0.5, r"LoTuS 정리에서는 $E(Y)$를 구할 때 $Y$의 PMF 따윈 필요 없게 되는데요, 그 이유는 Inverse image $g^{-1}(y)$를 잡고 식을 전개하기 때문입니다.$P_Y(y)$를 $x \in g^{-1}(y)$에 대한 시그마로 표현한 뒤 $E(Y)$에 때려박으면 식을 합성할 수 있습니다. 시그마 두 개를 어차피 모든 식에 $x$가 들어가니까 '모든 x에 대하여'라는 느낌의 마인드로 $x \in R_X$ 하나로 합쳐버리는 것이 핵심이에요. 결국 최종 식에는 $Y$의 PMF가 완전히 사라지게 됩니다."),
        ("망함", 0.0, r"$Y = g(X)$일 때 $E(Y)$ 구하는 데 $Y$ PMF 따윈 필요 없음.Inverse image $g^{-1}(y)$로 잡고 $P_Y(y) = \sum_{x \in g^{-1}(y)} p(x)$ 만든 다음에 $E(Y)$에 때려박으면 됨. 시그마 두 개 나오는 거 어차피 다 $x$로 표현되니까 '모든 x에 대하여' 같은 마인드로 $x \in R_X$ 하나로 합치면 끝임. 결국 $Y$의 PMF라곤 찾아볼 수 없는 식 $E(Y) = \sum g(x) P_X(x)$가 완성됨."),
    ]

    scoring(QUESTION4, None, CANDIDATES4, ne_metric, None)
    '''
    정상 0.90 / 절반 0.40 / 망함 0.20 | 판별력 0.70
    정상 0.90 / 절반 0.60 / 망함 0.10 | 판별력 0.80
    '''
    """

    QUESTION5 = r"$\int_{-\infty}^\infty$이 $\\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\\pi}$에서 사용됐습니다. 현재 페이지: Lem. 확률밀도함수에 쓰일 적분. 기호에 대해서 설명해주세요."
    CANDIDATES5 = [
        ("정상", 1.0, r"$\int_{-\infty}^\infty$ 기호는 주어진 수식 $\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}$ 내에서 피적분함수 $e^{-x^2}$을 음의 무한대부터 양의 무한대까지 전체 실수 영역에 대해 적분하라는 이상적분(Improper Integral) 범위를 지정하는 역할을 합니다. 또한 현재 페이지인 'Lem. 확률밀도함수에 쓰일 적분'에서는 이 적분이 정규분포 등의 확률밀도함수(PDF)를 정규화(Normalization)할 때 전체 확률의 합이 1이 되도록 적분 상수를 결정짓는 핵심 도구로 활용됩니다."),
        ("절반", 0.5, r"$\int_{-\infty}^\infty$ 기호는 주어진 수식 $\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}$에서 피적분함수 $e^{-x^2}$을 실수 전체 영역인 음의 무한대부터 양의 무한대 구간에 대해 적분하라는 이상적분 범위를 지정하는 역할을 합니다."),
        ("망함", 0.0, r"가우스 적분 공식에 따르면 exponential 함수 $e^{-x^2}$의 전체 적분 결과는 $\sqrt{\pi}$가 됩니다. 이는 확률밀도함수에서 매우 중요한 정규화 상수입니다."),
    ]

    scoring(QUESTION5, None, CANDIDATES5, se_metric, None)

    QUESTION6 = r"$\bigcup _{k=n}^\infty$이 $\bigcap _{n=1}^\infty \bigcup _{k=n}^\infty A_k$에서 사용됐습니다. 현재 페이지: Lem. Borel-Cantelli Lemma. 기호에 대해서 설명해주세요."
    CANDIDATES6 = [
        ("정상", 1.0, r"$\bigcup _{k=n}^\infty$ 기호는 주어진 전체 수식 $\bigcap _{n=1}^\infty \bigcup _{k=n}^\infty A_k$ 내에서 $n$번째 시점 이후의 사건들인 $A_n, A_{n+1}, A_{n+2}, \dots$에 대한 무한합집합을 형성하여, $n$ 이상의 어떤 시점 $k$에서 사건 $A_k$가 적어도 하나 발생함을 의미하는 부분 구조를 만듭니다.이 기호는 현재 페이지인 'Lem. Borel-Cantelli Lemma'에서 바깥쪽의 교집합 $\bigcap_{n=1}^\infty$과 결합하여 '사건 $A_k$가 무한히 많이 발생한다(infinitely often, i.o.)'는 상극한(limsup) 사건을 수학적으로 엄밀하게 정의하는 핵심적인 역할을 합니다."),
        ("절반", 0.5, r"$\bigcup _{k=n}^\infty$ 기호는 인덱스 $k$가 특정 자연수 $n$부터 시작하여 무한대로 갈 때, 해당 첨자를 갖는 집합들을 모두 합집합한다는 의미를 가진 기호입니다. 즉, $n$ 이상의 모든 인덱스 $k$에 대응하는 집합들의 원소를 모아놓은 무한합집합을 나타냅니다."),
        ("망함", 0.0, r"보렐-칸텔리 보조정리는 확률론에서 사건들의 급수 합이 수렴하거나 발산할 때, 해당 사건이 무한히 많이 일어날 확률이 0 또는 1이 된다는 법칙을 의미합니다."),
    ]

    scoring(QUESTION6, None, CANDIDATES6, se_metric, None)