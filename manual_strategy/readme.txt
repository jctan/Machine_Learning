'''
Student Name: John Tan 
GT User ID: jtan301
GT ID: 903366741

'''

1. To Run Manual Strategy Results of Part 1, 3, 4:

    Run on Terminal: PYTHONPATH=..:. python ManualStrategy.py

    - This will log the statisics of in-sample (Manual Rule-Based) and out-sample (Benchmark)
    - This will generate the charts of "SMA.png", "BBP.png", "Momentum.png", and "RSI.png"
    - This will generate the charts for both in-sample (Manual Rule-Based and Benchmark) of "in_sample_manual_benchmark.png"
      and out-sample (Manual Rule-Based and Benchmark) of "in_sample_manual_benchmark.png"


2. To Run Theoretically Optimal Strategy Results of Part 2:

   Run on Terminal: PYTHONPATH=..:. python TheoreticallyOptimalStrategy.py

   - This will log the statistics on terminal
   - This will generate the "theoretically_optimal_strategy.png" chart


3. Both TheoreticallyOptimalStrategy.py and ManualStrategy.py imports marketsimcode.py and indicators.py

    - marketsimcode computes the portfolio values, benchmarks, statistics, and dataframes
    - indidcators generates the indicators of SMA, BBP, Momentum, RSI, and both in-sample (Manual Rule-Based) and out-sample (Benchmark)



