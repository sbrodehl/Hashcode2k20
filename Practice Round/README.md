# \# Hash Code 2020 Practice Round

Solutions and code for the Practice Round of [Hash Code 2020](https://codingcompetitions.withgoogle.com/hashcode) **"More Pizza"**.  
The problem statement can be found [here](practice_problem.pdf).

The input files can be found in `input/`
- [example](input/a_example.in)  
    * Pizza types: `4`
    * Slices to order: `17`
- [small](input/b_small.in)  
    * Pizza types: `10`
    * Slices to order: `100`
- [medium](input/c_medium.in)  
    * Pizza types: `50`
    * Slices to order: `4,500`
- [quite big](input/d_quite_big.in)  
    * Pizza types: `2,000`
    * Slices to order: `1,000,000,000`
- [also big](input/e_also_big.in)  
    * Pizza types: `10,000`
    * Slices to order: `505,000,000`

#### Introduction

> You are organizing a Hash Code hub and want to order pizza for your hub’s participants.
> Luckily, there is a nearby pizzeria with really good pizza.
> The pizzeria has different types of pizza, and to keep the food offering for your hub interesting, you can only order at most one pizza of each type.
> Fortunately, there are many types of pizza to choose from!
> Each type of pizza has a specified size: the size is the number of slices in a pizza of this type.
> You estimated the maximum number of pizza slices that you want to order for your hub based on the number of registered participants.
> In order to reduce food waste, your goal is to order as many pizza slices as possible, but not more than the maximum number.
>
> _from [Problem statement for the Practice Round of Hash Code 2020](practice_problem.pdf)_

#### Task

> Your goal is to order as many pizza slices as possible, but not more than the maximum number.
>
> _from [Problem statement for the Practice Round of Hash Code 2020](practice_problem.pdf)_


#### Scoring

The solution gets 1 point for each slice of pizza ordered.
The total number of slices in the ordered pizzas must be less than or equal to the maximum number.

See the section on scoring in the [Problem statement for the Practice Round of Hash Code 2020](practice_problem.pdf) for more details.

## Algorithm

It's a basic [knapsack problem](https://developers.google.com/optimization/bin/knapsack).

## Scores

Overall **1,505,004,616** points.

#### A – example

* Pizza types: `4`
* Slices to order: `17`

_`16`_ points

#### B – small

* Pizza types: `10`
* Slices to order: `100`

_`100`_ points

#### C – medium

* Pizza types: `50`
* Slices to order: `4,500`

_`4,500`_ points

#### D – quite big

* Pizza types: `2,000`
* Slices to order: `1,000,000,000`

_`1,000,000,000`_ points

#### E – also big

* Pizza types: `10,000`
* Slices to order: `505,000,000`

_`505,000,000`_ points 
