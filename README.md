# Bounded strategic reasoning explains crisis emergence in multi-agent market games

![Poster](poster.png)

A version of this work was presented at the Summer Institute on Bounded Rationality 2022, at the Max Planck Institute in Berlin, Germany.

## Multi-agent Market Games
### How to run

Setup the market model
```python
from src.market import Market
market = Market(N=100, c=0.6) # Initialise the basic model
```

Then to run for T timesteps use

```python
market.run(T=1000)
```

Alternatively, run for an individual tick with
```python
market.tick()
```

Finally, to obtain the results dictionary call
```python
results = market.results()
```

For an example of how to run this work for multiple runs, see run.py

## Citation


