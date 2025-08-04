# Visualising the Vehicle Routing Problem (VRP)

This repo contains the current work-in-progress code for my Django web application that visualises the vehicle routing problem (VRP). 

A demo gif (Jul 2025):

![](img/v1_demo.gif)

Here is the problem description of the VRP, which  I took from [Vehicle Routing: Problems, Methods, and Applications (Second Edition) by Paolo Toth and Daniele Vigo.](https://epubs.siam.org/doi/book/10.1137/1.9781611973594)

> **Given**: A set of transportation requests and a fleet of vehicles.
> 
> **Task**: Determine a set of vehicle routes to perform all (or some) transportation requests with the given vehicle fleet at minimum cost; in particular, decide which vehicle handles which requests in which sequence so that all vehicle routes can be feasibly executed.

Mathematically, we are given the following:

| Notation | Description                                                                                                                                                     |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $O$      | Depot                                                                                                                                                           |
| $N$      | A customer set, where $N = \{1,2,...n\}$ and $\mid N\mid$ = n                                                                                                   |
|$S$|The customer subset, $S \subseteq N$|
| $q_i$    | The demand to the $i\text{th}$ customer, which we assume to be 1 in our simulation. If varied, then we are exploring the capacitated vehicle routing problem (CVRP) |
|$c_{ij}$|The cost of moving from location $i$ to location $j$|
|$K$ |The fleet of vehicles, $K = \{1,2, ...,\mid k\mid\}$|

Again, quoting from Toth and Vigo's textook, the vehicle routing problem can be split into two subproblems:

(i) Assigning which vehicle takes which locations. In other words, partitioning the customer set $N$ into feasible clusters $S_1, ... S_{\mid K \mid}$.

(ii) Solving a travelling salesman problem within each cluster. In other words, routing each vehicle through the locations in $S_k$, for $k \in K$, insisting that the route begins and ends at $O$.

The solution should minimise the overall sum of distances $c_{ij}$ for all routes. A fuller mathematical explanation of the VRP will be given on my blog when I find the time to write it.