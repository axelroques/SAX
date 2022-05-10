# Symbolic Aggregate approXimation (SAX) algorithm

Python implementation of the SAX algorithm from _Lin et. al. (2003)_.

This implementation takes a Pandas dataframe as an input. The dataframe must contain a `t` column containing the different timestamps. Apart from this restriction, this implementation is particularly useful as it allows to process multiple columns of data at once.

---

## Context

The SAX representation of times series is a symbolic representation. It allows dimensionality/numerosity reduction and to define a distance measure that lower bounds the Euclidian distance, directly on the discretized time series.

There are three main steps in the algorithm:

- **Normalization**. We use the Inverse normal transformation (INT algorithm to transform the sample distribution to a correct approximation of the normal distribution (see _Beasley et. al., 2009_).
- **Piecewise Aggregate Approximation (PAA)**. The PAA is used as a dimensionality reduction technique (see _Keogh et. al. 2001_). The PAA approximates the data by segmenting the sequences into equi-length sections and recording the mean value of these sections.
- **Discretization**. Given that the normalized time series have highly Gaussian distribution, we can simply determine the “breakpoints” that will produce a equal-sized areas under Gaussian curve. Once the breakpoints are computed, we can discretize a time series using the PAA representation: all PAA coefficients that are below the smallest breakpoint are mapped to the symbol _a_, all coefficients greater than or equal to the smallest breakpoint and less than the second smallest breakpoint are mapped to the symbol _b_, _etc_.

---

## Examples

Processing the data:

```python
df = pd.read_csv('your_data.csv')
sax = SAX(df, w=100, a=4)
sax.process()
```

The sax object now contains results from the different steps of the algorithm:

- sax.df_INT returns the dataframe after the normalization step.
- sax.df_PAA returns the dataframe after the PAA step.
- sax.df_SAX returns the dataframe after the discretization step.

It also contains the various SAX parameters:

- sax.w returns the number of segments in the PAA - and SAX - representation (after the dimensionality reduction).
- sax.a returns the number of symbols in the alphabet.
- sax.alphabet returns the different symbols in the alphabet (determined by parameter _a_).
- sax.breakpoints returns the values of the different breakpoints computed to discretize the time series.

Plotting the results:

```python
sax.plot_normalization(i_plot=1)
sax.plot_discretization(i_plot=1)
```

The _i_plot_ parameter can be modified to plot the desired column of the input dataframe. Only a single column can be plotted at a time to prevent having too many graphs at once.
