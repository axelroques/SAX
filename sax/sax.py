
from scipy.stats import norm
import pandas as pd
import numpy as np

from .discretization import discretization_step
from .plot import plot_INT, plot_PAA, plot_SAX
from .plot import plot_INT_subsequences, \
    plot_PAA_subsequences, \
    plot_SAX_subsequences
from .subsequence import generate_subsequences
from .int import INT_step
from.paa import PAA_step


class SAX:

    def __init__(self, df, w=10, a=3, alphabet_type='letters'):

        # Input data
        self.df = df

        # Convert time column to a pandas date_time
        self.df['t'] = pd.to_datetime(self.df['t'])

        # Representation parameters
        self.w = w
        self.a = a
        self.alphabet_type = alphabet_type
        if alphabet_type == 'letters':
            self.alphabet = np.array([chr(i) for i in range(97, 97 + a)])
        elif alphabet_type == 'numbers':
            self.alphabet = np.arange(a)
        else:
            raise RuntimeError(
                "Unexpected alphabet type. Expected 'letters' or 'numbers"
            )
        self.breakpoints = norm.ppf(np.linspace(0, 1, a+1)[1:-1])

    def process(self):
        """
        Whole series discretization process.
        """

        # Normalization
        self.df_INT = INT_step(self.df)

        # PAA
        self.df_PAA = PAA_step(self.df_INT, self.w)

        # Discretization
        self.df_SAX = discretization_step(self.df_PAA,
                                          self.alphabet,
                                          self.breakpoints)

    def plot_normalization(self, i_plot=1):
        """
        Plots the results from the INT step.
        """

        # Plot parameter
        self.i_plot = i_plot
        plot_INT(self)

        return

    def plot_discretization(self, i_plot=1):
        """
        Plots the results from the PAA and discretization step.
        """

        # Plot parameter
        self.i_plot = i_plot

        plot_PAA(self)
        plot_SAX(self)

        return


class SAX_subsequences:

    def __init__(self, df, w=10, a=3, alphabet_type='letters', n=None, k=None):

        # Input data
        self.df = df

        # Convert time column to a pandas date_time
        self.df['t'] = pd.to_datetime(self.df['t'])

        # Symbolic representation parameters
        self.w = w
        self.a = a
        self.alphabet_type = alphabet_type
        if alphabet_type == 'letters':
            self.alphabet = np.array([chr(i) for i in range(97, 97 + a)])
        elif alphabet_type == 'numbers':
            self.alphabet = np.arange(a)
        else:
            raise RuntimeError(
                "Unexpected alphabet type. Expected 'letters' or 'numbers"
            )
        self.breakpoints = norm.ppf(np.linspace(0, 1, a+1)[1:-1])

        # Optional segmentation parameters
        self.n = n
        self.k = k

    def process(self):
        """
        Subsequence discretization: extract subsequences of 
        length n from the time series, normalize the 
        subsequence and convert each subsequence into a 
        SAX word.
        """

        # Generate subsequences of length
        self.subsequences = generate_subsequences(self.df,
                                                  self.n,
                                                  self.k)

        # SAX process for each subsequence
        self.df_INT = []
        self.df_PAA = []
        self.df_SAX = []
        for subsequence in self.subsequences:

            # Normalization
            self.df_INT.append(INT_step(subsequence))

            # PAA
            self.df_PAA.append(PAA_step(self.df_INT[-1], self.w))

            # Discretization
            self.df_SAX.append(discretization_step(self.df_PAA[-1],
                                                   self.alphabet,
                                                   self.breakpoints))

        return

    def plot_normalization(self, i_plot=1):
        """
        Plots the results from the INT step.
        """

        # Plot parameter
        self.i_plot = i_plot
        plot_INT_subsequences(self)

        return

    def plot_discretization(self, i_plot=1):
        """
        Plots the results from the PAA and discretization step.
        """

        # Plot parameter
        self.i_plot = i_plot

        plot_PAA_subsequences(self)
        plot_SAX_subsequences(self)

        return
