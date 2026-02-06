Metrics & statistics:
- frequency of each winner
- Condorcet winner existence and whether rule picks Condorcet
- social welfare (sum of utilities) for chosen alternative(s)
- manipulability stats: fraction of profiles where a profitable manipulation exists
- average margin of victory, number of ties
- runtime per trial, memory usage

Tests & validation:
- unit tests for paradoxes (e.g. Condorcet cycle, Borda counterexample)
- property tests for monotonicity, pareto optimality
- vectorized results VS naive per-voter loop implementation for correctness on randomized small inputs