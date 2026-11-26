---
scope: Course map for the hands-on course on 『밑바닥부터 시작하는 딥러닝』 chapters 1 to 6
authority: Decisions from the grilling session of 2026-11-26 (user approved every item). The session handoff is ../../notes/handoff-dlfs-course.md
status: Plan. No stage has started
read_when: before you run or change any stage of the course
---

# DLfS course map (chapters 1 to 6)

Reference document. The course grows one small network over five stages.
Each stage removes a pain that the previous stage made the user feel.
The user experiences each concept first. He reads the book at the end of the day.

```
stage 1     stage 2       stage 3           stage 4          stage 5
ch1-2   ->  ch3       ->  ch4          ->   ch5         ->   ch6
gates       forward       loss + numeric    backprop         optimizers,
by hand     on toy data   grad training     layers           init, BN, Dropout
```

## Rules for every stage

- Write each script in the session, when the stage needs it. Do not pre-write scripts.
- The user types each script (transcription mode). Keep a script short: one idea, one run.
- Before each run, the user predicts an output value or shape. Then he runs it and compares.
- Continue the Q&A until he explains the result in his own words.
- Use toy data only. Do not write code for the `mnist` TODOs (`Affine`, `ReLU`, `SoftmaxWithLoss`, `SGD`, `train()`). The LMS forbids AI-generated code for a whole TODO function.
- Put scripts in this directory as `sN_<topic>.py`. Save plots as PNG next to the script.
- Run with `../../.venv/bin/python` (Python 3.12, numpy, matplotlib, pytest). Call `matplotlib.use("Agg")` before `pyplot`.
- At the end of each stage, run the glossary step and fill the stage sheet. See "End of each stage".

## Shared toy data

Stages 2 to 5 use one data set: a 2-D spiral with 3 classes, about 100 points per class, made with numpy and a fixed seed.
A straight line cannot split the spiral, so the user sees why a hidden layer and a nonlinearity matter.
Write `toy_data.py` at the start of stage 2. Each later stage imports it.

## Stage 1: chapters 1 and 2 (NumPy, perceptron)

Question: what can a weighted sum and a threshold do, and where does it stop?

- NumPy: `shape`, broadcasting, and the shape rule of `@` (`(N, D) @ (D, H) -> (N, H)`).
- AND, NAND, and OR gates with hand-picked `w` and `b`.
- XOR fails for one perceptron. Plot the decision line on the four points.
- XOR with two layers: NAND and OR, then AND.

Pain for the next stage: the user picks every weight by hand, and the step function has no slope.

Glossary candidates: `shape`, broadcasting, `W`, `b`, perceptron, linear separability.

Book: 1.5 넘파이, 1.6 matplotlib, 2.1 to 2.5.

## Stage 2: chapter 3 (forward pass)

Question: how does an input become a class score, and what is each array's shape?

- Plot the step function, sigmoid, and `ReLU`.
- Two linear layers with no activation equal one linear layer. Show it with numbers.
- A 3-layer forward pass with matrices. Print the shape after every layer, with batch size `N` first.
- `logits` versus probability. Softmax, the overflow of `np.exp(1000)`, and the max-subtraction fix.
- Softmax does not change `argmax`.
- Random weights on the spiral give about 33% accuracy.

Pain for the next stage: no number says how bad the weights are, and no rule says how to change them.

Glossary candidates: `logits`, `Affine`, `ReLU`, activation function, softmax, batch.

Book: 3.1 to 3.6. Section 3.6 uses MNIST with trained weights from the book. The user can skim it.

**Time check at the end of stage 2.** The budget is 6 hours in total. If the course is late, cut stage 5 to the optimizer comparison only. Never cut stage 4.

## Stage 3: chapter 4 (loss and numerical gradient)

Question: how does one number tell the network which way to move?

- Cross-entropy error for one sample. `np.log(0)` gives `-inf`, so clip the probability (`np.clip(p, 1e-7, 1.0)`).
- Average over the batch.
- Change one weight by a small amount: accuracy stays the same, but loss changes. This is why training uses loss, not accuracy.
- Central-difference numerical derivative. Gradient descent on `f(x0, x1) = x0**2 + x1**2`.
- Learning rate too large and too small. Plot both paths.
- Train a 2-layer network on the spiral with numerical gradients and minibatches. Measure the time per step. Save the loss curve.

Pain for the next stage: each step needs 2 forward passes per parameter. Count them.

Glossary candidates: loss, cross-entropy error, gradient, learning rate (`lr`), minibatch, epoch, numerical derivative.

Book: 4.1 to 4.5.

## Stage 4: chapter 5 (backpropagation)

Question: how do we get every gradient from one backward pass?

- The computational graph of the book's apple example. Multiply and add nodes, by hand first.
- The chain rule along the graph.
- Layers with `forward` and `backward` that store state: a multiply layer and an add layer.
- `ReLU` backward with `mask`. Sigmoid backward.
- `Affine` backward: derive `dW`, `db`, and `dx` from the shapes. `db` sums over the batch.
- Softmax-with-loss backward gives `(y - t) / N`.
- Gradient check against the stage 3 numerical gradient. Then break one backward line on purpose and see the check fail.
- Train the same network as stage 3. Compare the time per step.

The toy layers in this stage are not the `mnist` classes. Use different names (for example `ToyAffine`), and keep the shapes and formulas visible on paper first.

Glossary candidates: computational graph, chain rule, `dout`, `mask`, `dW`, `db`, gradient check, backpropagation.

Book: 5.1 to 5.7.

## Stage 5: chapter 6 (training techniques)

Question: what makes training fast and stable, beyond plain SGD?

- SGD, Momentum, AdaGrad, and Adam on `f(x, y) = x**2 / 20 + y**2`. Plot the four paths.
- The same optimizers on the spiral. Plot the loss curves.
- Weight initialization: activation histograms of a 5-layer network with std 1, std 0.01, Xavier, and He.
- Overfitting with a small training set. Then Dropout. BatchNorm only if time remains.

Cut version: the optimizer comparison only. In `mnist`, Adam, BatchNorm, and Dropout are provided code.

Glossary candidates: optimizer, Momentum, Adam, weight initialization, He initialization, overfitting, `Dropout`, `BatchNorm`.

Book: 6.1 to 6.5.

## End of each stage

- Glossary step (about 10 minutes): offer the candidates. The user picks 3 to 5. For each term, he writes a definition in his own words. Attack the definition with counterexamples and edge cases. Record the term in `../../GLOSSARY.md` § 신경망 (mnist) only when the definition holds. The entry keeps his Korean definition as he wrote it, then one English line under it (user said 2026-11-26).
- Term spelling: if a code name or `statement-1326.md` has the term, use that spelling (`logits`, `Affine`, `SoftmaxWithLoss`). Otherwise use the book's Korean term.
- Fill the stage sheet in `../../notes/sheets/mnist/dlfs-N-*.md`: what he confirmed, open questions, book sections.

The book section numbers come from the agent's memory of the Korean edition, not from the book. Confirm them against the book's table of contents at the first stage.
