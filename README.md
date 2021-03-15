In this assignment, I will follow Bailey, David and Lopez de Pardo(2012): 'Balanced baskets: a new approach to trading and hedging risks' *Journal of Investment Strategies (Risk Journals)* Vol. 1 No. 4 pp. 21-62

**General Setting**

Suppose we have $n$ instruments to create a portfolio, we have their covariance matrix $V$ and weights on each instruments $\omega$, a most common way to construct a basket is to minimize its variance subject to the asset already in hold, that is to minimize $\sigma_{\Delta B}=w'Vw$.

But it poses some problem since the risk contributed by each leg is not equal, so in case of sudden structural break in one of its legs, the overall portfolio may suffer larger variance than expected. Hence the idea of 'balanced' basket is introduced, the key idea is to allocate assets such that the contribution of each leg to overall risk is somehow equivalent while keeping the overall exposure low.  

**Contribution to Risk(CtR)**

The author introduced a measure of individual instrument's contribution to the basket's variance. First, we recall the famous Euler's Theorem, which states that if $f(x)$ is a $t$-order homogeneous function of $x$, then $tf(x) = \sum x_if_i$. Now notice that the standard deviation $\sigma_{\Delta B}$ is a first order homogeneous function of $\omega$, we have $ \sigma_{\Delta B} = \sum \omega_i \frac{\partial\sigma_{\Delta B}}{\partial w_i}$ , adding a normalization factor we define the contribution of risk of instrument $i$ to be:
$$
CtR_i=\frac{\partial\sigma_{\Delta B}}{\partial w_i}\frac{\omega_i}{\sigma_{\Delta B}}=\frac{\sigma_{\Delta B,\Delta S_i}}{\sigma_{\Delta B}^2}=\frac{\omega_i(V\omega)_i}{\sigma_{\Delta B}^2}
$$

**Equal Risk Contribution (ERC) Problem**

The traditional risk minimization problem may result in a portfolio that

The ERC weight we are seeking is one that has equal CtR for each instrument, that is $\omega_{ERC}$ satisfies
$$
CtR_i = \frac{1}{n}\space\space\space\forall 1\leq i\leq n
$$

**Taylor's Expansion for CtR **

The article derives the first two gradient of CtR, which is needed for a numerical solution of ERC problem, the result is presented below:
$$
\Delta CtR_i \approx [\frac{\omega_i\sigma_i^2}{\sigma_{\Delta B}^2}(1-2\rho_{\Delta B,\Delta S_i}^2)+\frac{\sigma_i\rho_{\Delta B,\Delta S_i}}{\sigma_{\Delta B}}]\Delta \omega_i
\\+[\frac{\sigma_i^2}{\sigma_{\Delta B}^2}(1-2\rho_{\Delta B,\Delta S_i}^2)-\rho_{\Delta B,\Delta S_i}\frac{\omega_i \sigma_i^3}{\sigma_{\Delta B}^3}(2-3\rho_{\Delta B,\Delta S_i}^2)](\Delta \omega_i)^2
$$
If we let 
$$
\begin{aligned}
a =& \frac{\sigma_i^2}{\sigma_{\Delta B}^2}(1-2\rho_{\Delta B,\Delta S_i}^2)-\rho_{\Delta B,\Delta S_i}\frac{\omega_i \sigma_i^3}{\sigma_{\Delta B}^3}(2-3\rho_{\Delta B,\Delta S_i}^2)
\\b=&\frac{\omega_i\sigma_i^2}{\sigma_{\Delta B}^2}(1-2\rho_{\Delta B,\Delta S_i}^2)+\frac{\sigma_i\rho_{\Delta B,\Delta S_i}}{\sigma_{\Delta B}}
\\c =& -\Delta CtR_i
\end{aligned}\tag{1}
$$
We have the following
$$
a(\Delta\omega_i)^2+b\Delta\omega_i+c=0
$$
To make the approximation more accurate, we will always opt for a smaller $\Delta\omega_i$, thus we have the following expression for $\Delta\omega_i$
$$
\Delta\omega_i = \begin{cases}
\frac{-b+\sqrt{b^2-4ac}}{2b}&a\neq0, b\geq0\\
\frac{-b-\sqrt{b^2-4ac}}{2b}&a\neq0, b<0\\
-\frac{c}{b}&a=0
\end{cases}\tag{2}
$$

**A greedy algorithm is proposed to solve ERC problem**

1. Generate the initial asset allocation $w^0$ and calculating the respective CtR for each instrument
2. Suppose we already have $\omega^n$, Find the index $i$ that maximizes $|\frac{1}{n}-CtR_i|$, and compute $a,b,c$ according to (1), in this case $c = CtR_i-\frac{1}{n}$. Calculate $\Delta\omega_i$ according to (2), and let $\omega^{n+1}=\omega^{n}+\Delta\omega_i\textbf{e}_i$
3. Repeat 2 until the result reaches acceptable precision or the iteration exceeds a pre set limit.

The python code is implemented in ERC.py

This method, however, is not mathematically sound, since there is no guarantee for the accuracy of approximation using first two derivatives and the equations established in (2) is not always valid, since there is no guarantee on the solvability of equation (1). So this greedy algorithm is not as sound as the author describes. A more mathematically secure method can be seen in Xi Bai, Katya Scheinberg and Reha Tutuncu(2016): 'Least-squares approach to risk parity in portfolio selection' *Quantitative Finance*, Vol. 16, pp357-376, where they considered equal risk contribution portfolio construction from the perspective of sequential quadratic optimization.
 
 
