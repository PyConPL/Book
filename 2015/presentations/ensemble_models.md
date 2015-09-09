#Building better machine learning models: Power of ensembles

For a data platform, the quality of the machine learning model's output is one of the most critical pieces for its success.

Data, more often than not, is messy. But once one gets past the preliminary data clean-up, building an initial machine learning model isn't difficult. But how far is that from the optimal model? One of the core tenets in machine learning is that there is no substitute for domain expertise; that a simpler model with the right features will invariably outperform a complex model without the right features. 

When solving a typical machine learning problem, once most of the necessary data are collated and preliminary data cleansing work is done, figuring out the right features, feature transformations and models are as much art as science. This is so because the solution space to search and prune grows exponentially as you start considering all feature transformations and combinations of features along with multitude of model parameters. 

But what if there's a clever algorithmic way to search the solution space? This article covers one such important toolkit: ensemble learning. 

### Success Stories

Before going into what ensemble models are, it has to be mentioned that they are widely used in practice and are often instrumental in breaking into new thresholds. A couple of their successful use cases are:


* Ensemble models improved the baseline movie recommendation by 10% and won the  Netflix million-dollar prize
* Almost all recent [Kaggle](https://www.kaggle.com/) competitions are won by employing ensemble models. For example, see [here](https://github.com/ChenglongChen/Kaggle_CrowdFlower) 


### What are Ensemble Models?
>This is how you win ML competitions: you take other peoples’ work and ensemble them together.” [Vitaly Kuznetsov](http://cims.nyu.edu/~vitaly/) NIPS2014


The theoretical underpinning is that consensus information from diverse model outputs are more reliable than a single model. 
 At its core, an ensemble model structure looks like figure 1.

*figure 1: Ensemble model structure*
![alt text](ensemble_1.png)

Multiple model outputs are combined to create the final prediction. The individual(single) models are called base models. How the various base models are combined(ensembled) to create the final prediction determines the quality/accuracy of ensemble learning.

The key ingredient to ensemble is to select the base models with significant diversity in their predictions. If the individual base learners are similar, they add little information. Worse, they tend to reinforce the same error present within them.

###Motivation Example
Before going into the various ways of ensembling, let's take a step back and realize that ensembles do work with a simple example.

Let's consider an example of classifying a credit card transaction as fradulent or not. The prediction has to be made on 10 transactions. Let's take the case where we already know those 10 cases to be fradulent. Encoding 1 as fradulent and 0 as not-fraudulent, let there be three base model ouputs, one each from Logistic Regression, Random Forest and Gradient Boosting, each having 70% accuracy. 

While individual models have 70% accuracy, consider a simple way of ensembling them: Majority voting. Using majority voting scheme as the ensembling function, the prediction accuracy is boosted from 70% to 90%. Case 6 alone will remain mis-classified, as shown in Table 1.


*Table 1:Example output from three models*

|`RandomForest` | `xgboost` | `LogisticRegression`|EnsembledOutput|
|:------:|:-------:| :---------:|:------:|
| 0           | 1       |      1            | 1  |
| 1           | 1       |      0            | 1  |
| 1           | 0       |      1            | 1  |
| 1           | 1       |      0            | 1  |
| 1           | 1       |      1            | 1  |
| 0           | 0       |      1            | 0  |
| 1           | 1       |      0            | 1  |
| 1           | 1       |      1            | 1  |
| 1           | 0       |      1            | 1  |
| 0           | 1       |      1            | 1  |


A key point to be stressed again is that model diversity is important. If the models were similar, the output would've been similar and there would've been no improvement i the output. 
 
###Advantages
 Some of the advantages of using ensemble models are:
 
* **Improved accuracy**: Dozens of models, even of mediocre quality, may produce top-notch predictions as a team.
* **Robustness**: more robust than a single model
* **Efficiency**: A divide-and-conquer paradigm. Complex problem is decomposed into many sub-problems and then solved
* **Parallelization**: It naturally lends itself to parallelization.
* **Wider search of solution space**: When ensembling, different solution spaces searched by individual models are combined, leading to a wider search of solution space. Since the combination step is not computationally intensive, the search is more efficient than a single model searching the entire solution space.
* **Reduces overfitting**




### Different ways to create ensemble models


####Base Models

Let's now discuss some of the ways to create the base models, to ensure that they have enough diversity

1. **Different training sets**: If there's enough data, the same model can be run on different training examples. In practice, transformation of original training set is carried out to create multiple training sets. (*Widely used*)
2. **Different algorithms/algorithm diversity**: Choose diverse algorithms. `LinearRegression`, `LogisticRegression` are diverse from `DecisionTree`, `RandomForest` etc (Regression Vs Tree-based). `SVM` is another class of algorithms. Also, `Regression` could be L1 or L2. The basis function for `SVM` could be radial or linear.  (*Widely used*)
3. **Different parameter setups**: Called the hyperparameters, the parameters of the model can be varied to obtained different model outputs. An example would be to build `RandomForest` with shallow trees versus building it with denser trees (less trees vs more trees) (*Widely used*)
4. **Algorithm randomization**: A lot of the models have randomness playing a key part and the model can be run with different random initialization. (*Not so widely used*)
5. **Feature Sampling** Using subset of columns for different model runs produce different model outputs and can help in estimating and containing variance of model predictions(*Widely used*)


#### Model Aggregation

Some of the ways to aggregate the models are

1. **Voting/Averaging**: A simple way to aggregate output is to either take the candidate with maximum outputs or the average of outputs (if regression or probability is the desired output). For simple averaging, all models are assumed equal.
3. **Weighted voting/averaging**: The model is given a weight and the output is weighted based on that. An example would be: A model with higher accuracy has a higher weight than a model with lower accuracy.
4. **Using as attributes**: The model outputs are used as inputs for a second-stage model. See *stacking*
5. **Bagging**: **B**ootstrap **Agg**regat**ing** -Base model is created using bootstrap samples of training set and are combined by plain voting. `RandomForest` uses bagging.  
6. **Stacking**: Using different algorithms as base learners, the model outputs are used as meta attributes for another model. Also called *Stacked Generalization*. Currently, these are widely used. *An example of stacking*: Divide the dataset into two. Using the first half, build `LogisticRegression`, `SVM`, `LinearRegression`, `xgboost`, `RandomForest` models. Predict the output for the second half of the dataset. Using these meta attributes as input features, build a `LogisticRegression` model on the second half of the dataset. 

###Disadvantages of ensemble models

1. Model human readability is not great. While there are ways to show variable importance, they are not as interpretable as a simple `LinearRegression` model or a `DecisionTree` model. 
2. For some business cases, the tradeoff in time/effort it takes to build complex ensemble models may not be offset by the improvements in accuracy and hence may not be justified.

### Some Python libraries to aid efficient ensembling

1. `Pipeline`: This creates a pipeline of transforms with a final estimator. An example of pipeline could be: pre-processing(capping, standardizing, scaling) -> feature extraction(principal components, transformation) -> model creation.  The process can be made elegant and efficient using this.

2. `hyperopt`: It uses a form of bayesian optimization called *tree of Parzen estimators*. For weighted averaging of the base models, this is an efficient package for optimally identifying the models and their weights. In many cases, it may not be possible to specify the required objective function for the base models, but `hyperopt` allows custom objective function to be specified and so, ensures that the final ensembled model is optimized on the required objective function. 

3. `RandomizedSearchCV`: While we didn't talk about hyper-parameter optimization, this helps in efficient searching of hyper-parameters for the model. When running dozens of models as base models, it may not be possible to do an exhaustive grid search of hyper parameters (and in some cases, not tractable too). Randomized search of the hyper-parameter space helps in producing better model parameters, and hence better base model outputs.
4. `joblib`: For parallel computing. Different models can be run in parallel. 


### References
1. http://ews.uiuc.edu/~jinggao3/sdm10ensemble.htm
2. http://www.overkillanalytics.net/more-is-always-better-the-power-of-simple-ensembles/
3. http://www.rms.com/blog/2013/10/08/a-weight-on-your-mind/
4. http://mlwave.com/kaggle-ensembling-guide/
5. http://fastml.com/optimizing-hyperparams-with-hyperopt/
