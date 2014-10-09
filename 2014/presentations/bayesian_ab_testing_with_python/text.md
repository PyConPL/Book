# Bayesian A/B testing with Python - Bogdan Kulynych

## Introduction

A/B testing is a simple yet powerful instrument to evaluate design decisions for web applications. It's a kind of behavioral research study akin to clinical trials, conducted to assess the effectiveness of alternative variations of graphical designs, wording solutions, logical decisions in terms of different performance metrics. It is to be contrasted to _personalization_: the goal of A/B testing is to find a solution that fits best to all users, whereas personalization aims to find a best solution for every particular user.

Traditionally, a classical framework of statistical hypothesis testing is used to evaluate the performance of variations. This text discusses the Bayesian approach to A/B testing, its pros and cons, and a way of  implementing it using Python's `scikit` and an author's library called [`trials`](https://github.com/bogdan-kulynych/trials).

## Classical approach

Suppose there are two different variations of the landing web page design: call them A and B. A common problem is to find the one that will probably produce more sign-ups based on  collected data.

Within the classical frequentist approach, the following model is commonly used. Let $A$, $B$ be two independent finite binary populations corresponding to all possible page views by target audience. Each item in population is either a $1$ (success, user viewed the page and signed up) or $0$, (failure, user viewed the page and didn't sign up). We assume that both populations are Bernoulli-distributed  with *fixed parameters* $p_A, p_B$. We don't know the parameters, but want to estimate them. This is an important point that will be returned to later: the parameters are *fixed yet unknown*. 

We conduct an experiment by randomly showing the users different designs and logging the results. Sample data $X_A=\{x_A^{(i)}\}$, and $X_B=\{x_B^{(i)}\}$ are obtained, where $x_*^{(i)} \in \{0, 1\}$. We assume that every observation $x_A^{(i)}$, $x_B^{(i)}$ is randomly picked from the respective population in such a way that every item in population has an equal chance to be picked, i.e. $X_A$ and $X_B$ are randomly sampled from respective populations. Therefore, $x_A^{(i)} \sim \text{Bern}(p_A)$, $x_B^{(i)} \sim \text{Bern}(p_B)$. Moreover, this means that all  observations $x_A^{(i)}$, $x_B^{(i)}$ are independent. This is a strong assumption that almost never holds in real life. It is natural that there exist some common factors that influence multiple observations (for example, geographic location, time zone, screen size, etc.). If the influence of these factors is quite substantial, then probably this model isn't best fit for the task.

One way to reason about the true population parameters $p_A$ and $p_B$ is to use two-sample [t-test](https://en.wikipedia.org/wiki/Student%27s_t-test). We will test the null hypothesis about the equality of expected values of A and B: $$ H_0: p_A = p_B\ \Rightarrow\ p_A - p_B = 0 $$ Since $p_A$, $p_B$ can be estimated by sample means $\hat p_A = \bar X_A$, $\hat p_B = \bar X_B$, the distribution of the test statistic $T = \frac{\bar X_A - \bar X_B}{\sigma_{\hat p_A - \hat p_B}}$ (standardized $\hat p_A - \hat p_B$) approaches standard normal as the number of observations gets large, and approximately equals the Student's t-distribution if the number is not large enough. It is straightforward to find the value of the test statistic, knowing a formula for estimated variance:
$$\sigma_{\hat p_A - \hat p_B}^2 = \frac{\sigma_{X_A}^2}{n_{X_A}} + \frac{\sigma_{X_B}^2}{n_{X_B}}$$

And for the number of degrees of freedom $\nu$ of the t-distribution: 
$$ \nu = \frac{(\sigma_{X_A}^2/n_{X_A} + \sigma_{X_B}^2/n_{X_B})^2}{(\sigma_{X_A}^2/n_{X_A})^2/(n_{X_A}-1) + (\sigma_{X_B}^2/n_{X_B})^2/(n_{X_B}-1)}. $$

([Welch–Satterthwaite](https://en.wikipedia.org/wiki/Student%27s_t-test#Equal_or_Unequal_sample_sizes.2C_unequal_variances) formula, for the the most general case).

Then we find corresponding data likelihoods under the null hypothesis $P(X~|~H_0)$. An $\alpha$-confidence interval for the test statistic can be obtained as well: $\{ T \pm \sigma_{\hat p_A - \hat p_B} \cdot t_{\nu, \alpha}\}$.

In practice, if the number of observations is big enough, z-test is often conducted instead, i.e. the $T$-statistic is assumed to be normally distributed.

To control the false positive rate we use $\alpha$ (usually $5\%$), which actually equals to the probability of a false positive $\text{P}(|T| < t_{\nu,\alpha}~|~\neg H_0 ) = \alpha$. The probability of a false negative $\text{P}(|T| \geq t_{\nu,\alpha}~|~H_0)$ is a called a power function of the test. For t-test, it depends on difference between $p_A$ and $p_B$ and the number of observations. The larger is the number of observations and the larger is the difference between parameters, the smaller false negative rate is. For example, if the relative difference between true population parameters is small, e.g., 1%, around 80,000 observations is needed to provide at least 20% false negative rate. If the difference is 50%, 1000 is enough.

### Problems

Frequentist treats a probability as a frequency of an event's occurrence in a number of repeated experiments. Frequentist techniques rely greatly on the Law of Large Numbers and Central Limit Theorem. For A/B testing we would want to get the results as quickly as possible, possibly before the CLT can be applied.

There's also a philosophical issue with hypothesis testing: it answers the wrong question. For the example above, what we would like to do is estimate the true population parameters based on the observed data. In other words, we want to know something like $\text{P}(p_A > p_B~|~X)$. That formula doesn't make much sense within the frequentist paradigm, since probability is a frequency of an event in series of repeated experiments, yet $p_A$ and $p_B$ are *fixed* values, they're not outcomes of any experiments, not random variables, therefore, you can't make any probabilistic statements about them. The only thing hypothesis testing can provide is the likelihood of the data given the hypothesis, $\text{P}(X~|~p_A > p_B)$. We need to pick a hypothesis, then check how well the obtained data supports it. That makes sense, but the inverse $\text{P}(H~|~X)$ would fit our question so much better. In fact, the two probabilities $\text{P}(X~|~H)$ and $\text{P}(H~|~X)$ are connected by the Bayes rule, but one first has to change the definition of probability to apply it.

From a Bayesian perspective, probability is nothing but a degree of belief on a scale from 0 to 1. This interpretation not only drops the requirement for large repeated experiments, but allows to answer the question directly: what are our best estimates on population parameters given what we can observe. 

## Bayesian approach

Whereas $p_A, p_B$ where fixed population parameters in the previous model, for Bayesian approach let $p_A, p_B$ be independent random variables. The data now should be considered fixed. Previously, it was vice versa: parameters were fixed, and data was random; now parameters are random variables, and data is fixed.

Let _prior_ distributions of $p_A$ and $p_B$ be Beta-distributed:
$$p_A \sim \text{Beta}(\alpha_A, \beta_A),\ p_B \sim \text{Beta}(\alpha_B, \beta_B)$$ The choice of Beta distribution will be explained  later. Let number of sign-ups $k_A = |\{x_A^{(i)}=1\}|$, number of page views $n_A = |X_A|$. Assume that the likelihood of data obtained by logging views and sign-ups is binomial:  $\text{P}(X_A ~|~ p_A) = \text{Binomial}(k_A; n_A, p_A)$. Analogically, for B.

Applying Bayes theorem, we can find the posterior:
\begin{eqnarray*}
\text{P}(p_A ~|~ X_A) &=& \frac{\text{P}(X_A ~|~ p_A) \cdot \text{P}(p_A)}{\text{P}(X_A)} \propto \text{P}(X_A ~|~ p_A) \cdot \text{P}(p_A) \\
&=& {n_A\choose k_A} p_A^{k_A} (1-p_A)^{n_A - k_A}\ \frac{1}{B(\alpha_A, \beta_A) p_A^{1-\alpha_A} (1-p_A)^{1-\beta_A}} \\
&=& \text{Beta}(\alpha_A + k_A, \beta_A + n_A - k_A)
\end{eqnarray*}

The nice result in the final step occurs because Beta is a conjugate prior to Bernoulli and Binomial distributions, and this is the reason why it was chosen as a prior for $p_A$ and $p_B$. 

From the posterior distribution we can find interesting values like $P(p_A > p_B ~|~X)$, $P(p_A < p_B ~|~ X)$, and e.g., _lifts_ $\frac{p_B - p_A}{p_A}$ and $\frac{p_A - p_B}{p_B}$, or pretty much any function we'd like using Monte Carlo techniques. 

This model relies on similar assumptions (independent Bernoulli trials, implied by Binomial likelihood), but doesn't rely on large numbers like the previous one. An important observation is that instead of finding $\text{P}(\text{data} ~|~ \text{hypothesis})$ for a set of predefined hypotheses about the parameters, we integrate over all possible values of parameters (hypotheses) and get $\text{P}(\text{parameter} ~| ~\text{data})$ using Bayes theorem. In such sense, this approach is a generalization of hypothesis testing. 

In the end, this approach doesn't suffer from the problems outlined previously. This comes at the cost of expensive MCMC computations for more complicated posteriors.

## Example

Suppose we've gathered some data. Say, variation A was viewed 44 times, and produced 2 sign-ups, and variation B was viewed 96 times and produced 11 sign-ups. Let's use `scipy` to calculate some statistics. 

    from scipy import stats

    data = {
        'A': { 'views': 42, 'signups': 2 },
        'B': { 'views': 85, 'signups': 11 }
    }

    posteriors = {
        variation: stats.beta(logs['signups'],
            logs['views'] - logs['signups'])
        for variation, logs in data.items()
    }

Calculate expected sign-up rate $\text{E}[p_A~|~X]$:

```python
posteriors['A'].mean()
```

Get $ \text{E}[p_A~|~X] = 5.81\%$, $\text{E}[p_B~|~X] = 13.37\% $.

Calculate 95%-credible intervals:

    lower = posteriors['A'].ppf(0.025)
    upper = posteriors['A'].ppf(0.975)

$ \text{P}(1.00\% < p_A < 14.41\%) = 0.95 $, 
$\text{P}(7.07\% < p_B < 21.28\%) = 0.95 $

<!-- Kwadrat: Zamienilem mathbb na blackboard dla ConTeXt -->
Monte Carlo approach to compute $P(p_B > p_A~|~X) \approx \frac{1}{n}\sum_i \blackboard{I}[y_A^{i} > y_B^{i}]$ and expected lift:
```python
import numpy as np

sample_size = 10000
samples = {
    variation: posterior.sample(sample_size) \
    for variation, posterior in posteriors.items()
}

dominance = np.mean(samples['B'] > samples['A'])
lift = np.mean((samples['B'] - samples['A']) \
    / samples['A'])
```

Variation B performs better, so $P(p_B > p_A) = 92.90\%$. Expected lift of sign-up rate under variation B is $+271.68\%$.

`trials` is a tiny library that does all of the above and a little bit more.

```python
from trials import Trials

test = Trials(['A', 'B'], vtype='bernoulli')

test.update({
    'A': (2, 40),
    'B': (11, 79),
})
```

Statistics supported by `trials` for Bernoulli experiments: expected posterior, posterior CI, expected lift, lift CI, empirical lift, dominance.

$\text{P}(p_A > p_B ~|~ X)$:
```python
dominances = test.evaluate('dominance')
```

Expected lift $\text{E}(\frac{p_B - p_A}{p_A} ~|~ X)$:
```python
lifts = test.evaluate('expected lift')
```

Lift 95%-credible interval:
```python
intervals = test.evaluate('lift CI', level=95)
```

## Conclusion

We showed how to do A/B testing the Bayesian way using sign-up rate as an example metric. The technique is flexible enough to use any kind of interesting metrics by changing the prior and posterior distributions appropriately. Log-normal posterior could be used to evaluate variations based on time users spent on a page, Poisson posterior for number of clicks users made, etc. One could choose "nice" conjugate priors and posteriors, but, essentially, any distributions can be used at the cost of MCMC computation. The Bayesian approach is more general than the usual hypothesis testing approach, doesn't rely on large numbers in theory, and produces results that are easier to interpret.
