
import pandas as pd
from .discretization import discretization_step
from .plot import plot_INT, plot_PAA, plot_SAX
from .int import INT_step
from.paa import PAA_step


class SAX:

    def __init__(self, df, w=10, a=3):

        # Input data
        self.df = df

        # Convert time column to a pandas date_time
        self.df['t'] = pd.to_datetime(self.df['t'])

        # Representation parameters
        self.w = w
        self.a = a

    def process(self):

        # Normalization
        self.df_INT = INT_step(self.df)

        # PAA
        self.df_PAA = PAA_step(self.df_INT, w=self.w)

        # Discretization
        self.df_SAX, self.breakpoints, self.alphabet = \
            discretization_step(self.df_PAA, a=self.a)

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
