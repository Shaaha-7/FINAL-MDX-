"""
data/question_bank.py
─────────────────────────────────────────────────────────────
10 ML/DS/AI skill areas × 3 difficulty levels (easy/medium/hard)
Each question is handcrafted for technical depth and interview realism.
─────────────────────────────────────────────────────────────
"""

from typing import Dict, List

QUESTION_BANK: Dict[str, Dict[str, List[str]]] = {
    "Bias-Variance Tradeoff": {
        "easy": [
            "What is bias in machine learning? Provide a concrete real-world example.",
            "What is variance in a model and how does high variance manifest in practice?",
        ],
        "medium": [
            "Explain the bias-variance tradeoff. How does model complexity influence each component?",
            "Walk me through how you would diagnose whether a production model has high bias vs. high variance.",
        ],
        "hard": [
            "Mathematically derive how the expected MSE decomposes into bias², variance, and irreducible noise. Prove why these terms are orthogonal.",
            "Compare bagging and boosting through the lens of bias-variance. Under what conditions does each fail to reduce the dominant error source?",
        ],
    },
    "Gradient Descent & Optimization": {
        "easy": [
            "Explain gradient descent intuitively. What problem is it solving and why does it work?",
            "What is a learning rate? Describe what happens when it is too large vs. too small.",
        ],
        "medium": [
            "Compare batch GD, stochastic GD, and mini-batch GD. What are the convergence and computational trade-offs?",
            "What are saddle points and plateaus? How do Adam, RMSprop, and momentum handle them differently?",
        ],
        "hard": [
            "Explain the convergence properties of SGD for non-convex objectives. What assumptions are needed and where do they break down in deep learning?",
            "Derive the Adam update rule from first principles. Why does bias correction matter in the early iterations?",
        ],
    },
    "Regularization": {
        "easy": [
            "What is overfitting and how does regularization combat it? Give an example from a real ML project.",
            "Describe L2 (Ridge) regularization. What does adding λ||w||² to the loss actually do to the weights?",
        ],
        "medium": [
            "Compare L1 (Lasso) vs. L2 (Ridge) regularization. When does Lasso produce sparse solutions and why?",
            "What is dropout? Explain the ensemble interpretation and why it reduces co-adaptation of neurons.",
        ],
        "hard": [
            "Derive the closed-form Ridge regression solution. Show how the regularisation term shifts the eigenspectrum and why this stabilises ill-conditioned systems.",
            "Design a regularisation strategy for a transformer fine-tuned on a 500-sample medical dataset. Justify every choice quantitatively.",
        ],
    },
    "Model Evaluation & Metrics": {
        "easy": [
            "Define precision, recall, and F1-score. Build a 2×2 confusion matrix and compute each from scratch.",
            "What is k-fold cross-validation and why is it superior to a single train/test split?",
        ],
        "medium": [
            "Explain ROC-AUC. What makes a classifier with AUC=0.70 better or worse depending on the business problem?",
            "You have a fraud detection model with a 99:1 class imbalance. What metrics matter and what pitfalls should you avoid?",
        ],
        "hard": [
            "Design a comprehensive evaluation framework for a multi-label classification system deployed in a hospital triage setting. What offline and online metrics would you track?",
            "Explain model calibration. How do you measure calibration error, and walk through how Platt scaling and isotonic regression fix it?",
        ],
    },
    "Feature Engineering": {
        "easy": [
            "Why is feature scaling important? Describe which algorithms require it and which are invariant to scale.",
            "Explain one-hot encoding vs. label encoding. When does label encoding introduce a subtle but serious bug?",
        ],
        "medium": [
            "A dataset has 30% missing values in a key feature. Walk through your complete strategy for handling this, including trade-offs.",
            "Compare filter, wrapper, and embedded feature selection methods. Which would you use for a 10,000-feature genomics dataset and why?",
        ],
        "hard": [
            "Design an end-to-end feature engineering pipeline for a time-series churn prediction problem with 50M rows, mixed types, and a 2-hour SLA. How do you prevent leakage?",
            "You suspect target leakage in a production model that shows 0.98 AUC. Describe your complete investigation and remediation strategy.",
        ],
    },
    "Deep Learning": {
        "easy": [
            "Explain backpropagation step by step. What is the chain rule's role and what does each gradient represent?",
            "Name three activation functions and explain the specific problem each was designed to solve.",
        ],
        "medium": [
            "Describe the vanishing gradient problem. How do ResNets, BatchNorm, and careful initialisation each address it from different angles?",
            "Contrast CNNs and RNNs architecturally. What inductive bias does each encode and where does each break down?",
        ],
        "hard": [
            "Derive the scaled dot-product attention mechanism mathematically. Why is the 1/√d_k scaling factor critical and what does attention entropy tell you about the model?",
            "You are training a 7B parameter LLM on 8 A100 GPUs. Walk through your complete distributed training strategy including gradient checkpointing, mixed precision, and ZeRO optimisation stages.",
        ],
    },
    "Statistics & Probability": {
        "easy": [
            "State the Central Limit Theorem precisely. Give two ML contexts where it is implicitly relied upon.",
            "Distinguish between probability and likelihood. Why does this distinction matter when fitting distributions?",
        ],
        "medium": [
            "A colleague reports p=0.049 as 'significant'. Name three ways this conclusion could still be wrong and how you would investigate each.",
            "Derive the MLE for logistic regression parameters. Show why the log-likelihood is concave and what that guarantees about optimisation.",
        ],
        "hard": [
            "Prove that MLE under a Bernoulli likelihood is equivalent to minimising cross-entropy loss. Extend this to multi-class softmax.",
            "You must choose between a Bayesian and frequentist approach for A/B testing a new recommendation model at 10M daily users. Defend your choice rigorously, including practical implementation details.",
        ],
    },
    "MLOps & Deployment": {
        "easy": [
            "What is model drift? Distinguish data drift from concept drift with a concrete example for each.",
            "Compare batch inference and real-time inference. What architectural choices differ between them?",
        ],
        "medium": [
            "Walk through a production-grade CI/CD pipeline for an ML model from code commit to serving, including automated testing and rollback strategy.",
            "Design an A/B testing framework for safely rolling out a new recommendation model. What metrics do you monitor and what are your stopping criteria?",
        ],
        "hard": [
            "Architect a real-time fraud detection system serving 100K transactions/second with p99 latency <10ms, high availability, and the ability to retrain daily without downtime.",
            "Your production model's AUC degraded from 0.92 to 0.78 over six months. Describe your complete root-cause analysis process and remediation plan.",
        ],
    },
    "NLP & Transformers": {
        "easy": [
            "What is tokenisation and why does it vary across GPT-4, BERT, and a character-level model? What are the trade-offs?",
            "Explain TF-IDF. Under what conditions does it outperform or underperform dense embeddings?",
        ],
        "medium": [
            "Explain how Word2Vec learns semantic similarity via the skip-gram objective. What linguistic relationships does it capture and where does it fail?",
            "Describe the transformer architecture end-to-end. What problem does positional encoding solve and why can't the attention mechanism solve it alone?",
        ],
        "hard": [
            "BERT uses masked language modelling for pre-training. Explain the training objective mathematically, describe the [CLS] token mechanics, and identify three fundamental limitations of BERT for generative tasks.",
            "You must fine-tune a 13B LLM for medical NER with only 200 labelled examples and a 16GB GPU budget. Compare LoRA, prefix-tuning, and full fine-tuning on this constraint set.",
        ],
    },
    "SQL & Data Engineering": {
        "easy": [
            "Explain INNER JOIN vs. LEFT JOIN. Write a query that returns all users who have never made a purchase.",
            "Your analytics table has duplicate rows. Write a complete SQL query to identify them and explain two approaches to remove them.",
        ],
        "medium": [
            "Write a SQL query to compute a 7-day rolling average of daily revenue, handling missing days correctly.",
            "Explain window functions. Show with code how ROW_NUMBER, RANK, DENSE_RANK, and LAG differ. Give a real analytics use-case for each.",
        ],
        "hard": [
            "Design a complete SQL schema for a collaborative filtering recommendation system. Write the query that generates candidate pairs for users who have not yet interacted.",
            "A query on a 500M-row fact table takes 4 minutes. Walk through your complete diagnostics: EXPLAIN plan analysis, index strategy, partitioning, materialised views, and when you'd escalate to a columnar store.",
        ],
    },
}

SKILLS: List[str] = list(QUESTION_BANK.keys())


# ── Pre-written ideal answers for common questions ────────────────
# Key = first 80 chars of the question text
IDEAL_ANSWERS: dict = {
    "What is bias in machine learning? Provide a concrete real-world example.": (
        "Bias is the error introduced by approximating a complex real-world problem with a simplified model — "
        "mathematically it is E[f̂(x)] - f(x), the difference between the model's expected prediction and the true function. "
        "High bias means the model systematically misses the signal regardless of the training data. "
        "Example: using linear regression to predict house prices when the true relationship is nonlinear — "
        "the model will consistently underestimate expensive houses and overestimate cheap ones across all training sets. "
        "The fix is to increase model complexity or use a more expressive model class."
    ),
    "Explain the bias-variance tradeoff. How does model complexity influence each component?": (
        "The expected MSE decomposes as Bias² + Variance + Irreducible Noise. "
        "Bias measures how far the average prediction is from the true value; variance measures how much predictions scatter across different training sets. "
        "As model complexity increases, bias decreases (model can fit more patterns) but variance increases (model overfits to noise in each dataset). "
        "Optimal complexity minimises their sum. Practically: a depth-1 decision tree has high bias (underfits), "
        "an unpruned tree on small data has high variance (overfits). "
        "Regularisation, ensembles, and cross-validated hyperparameter tuning navigate this tradeoff."
    ),
    "Explain gradient descent intuitively. What problem is it solving and why does it work?": (
        "Gradient descent minimises a loss function L(θ) by iteratively updating parameters in the direction of steepest descent: "
        "θ ← θ - α∇L(θ), where α is the learning rate. "
        "It works because the gradient points in the direction of maximum increase, so its negative points toward the minimum. "
        "For convex functions it converges to the global minimum; for non-convex (like neural nets) it finds local minima or saddle points. "
        "The learning rate controls step size — too large causes divergence, too small causes slow convergence or getting stuck."
    ),
    "What is a learning rate? Describe what happens when it is too large vs. too small.": (
        "The learning rate α controls the step size in each gradient descent update: θ ← θ - α∇L(θ). "
        "Too large: updates overshoot the minimum, loss oscillates or diverges. "
        "Too small: convergence is extremely slow, and the optimizer may get trapped in shallow local minima. "
        "In practice, learning rate schedules (cosine annealing, warm restarts) or adaptive methods (Adam, RMSprop) "
        "automatically adjust α. Typical starting values: 1e-3 for Adam, 0.01-0.1 for SGD with momentum."
    ),
    "Explain backpropagation step by step. What is the chain rule's role and what does each gradient represent?": (
        "Backpropagation computes gradients of the loss with respect to every parameter using the chain rule. "
        "Forward pass: compute activations layer by layer, storing intermediate values. "
        "Backward pass: starting from the loss, apply the chain rule recursively — "
        "∂L/∂W_l = (∂L/∂a_l) · (∂a_l/∂z_l) · (∂z_l/∂W_l), where each term is the local gradient at that layer. "
        "Each gradient ∂L/∂W tells us how much increasing that weight increases the loss. "
        "The key insight is that the chain rule allows efficient reuse of intermediate gradients, "
        "making the computation O(parameters) rather than O(parameters²)."
    ),
}
