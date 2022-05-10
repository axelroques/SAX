
import matplotlib.pyplot as plt
import numpy as np


def plot_INT(object):
    """
    Plots the normalization step.
    """

    from statsmodels.api import qqplot

    _, ax = plt.subplots(figsize=(13, 5))

    # Normalized time series
    ax.plot(object.df_INT['t'], object.df_INT.iloc[:, object.i_plot])
    ax.set_title(
        f'Inverse Normal Transformation - Column {object.df_INT.columns[object.i_plot]}')
    ax.set_xlabel('Time')
    plt.show()

    # QQ plots
    f = plt.figure(figsize=(13, 5))
    ax = f.add_subplot(1, 2, 1)
    qqplot(object.df.iloc[:, object.i_plot], line='45',
           ax=ax, c='royalblue', markersize=0.5)
    ax.set_xlabel('Normal Theoretical Quantiles')
    ax.set_ylabel('Data Quantiles')
    ax.set_title(
        f'QQ-plot - Original data\nColumn {object.df.columns[object.i_plot]}')

    ax = f.add_subplot(1, 2, 2)
    qqplot(object.df_INT.iloc[:, object.i_plot], line='45',
           ax=ax, c='royalblue', markersize=0.5)
    ax.set_xlabel('Normal Theoretical Quantiles')
    ax.set_ylabel('Data Quantiles')
    ax.set_title(
        f'QQ-plot - Normalized data\nColumn {object.df_INT.columns[object.i_plot]}')

    plt.show()

    return


def plot_PAA(object):
    """
    Plots the PAA representation.
    """

    _, ax = plt.subplots(figsize=(13, 5))

    for line in object.breakpoints:
        ax.axhline(line, c='crimson', alpha=0.4, ls='--', lw=0.7)

    # Plot text
    # dt = object.df_SAX['t'].iloc[1] - object.df_SAX['t'].iloc[0]
    # for t, letter in enumerate(df_SAX.iloc[:, i_plot]):
    #     ax.text(df_PAA['t'].iloc[t]+dt/2,
    #             df_PAA.iloc[t, i_plot]+0.1,
    #             f'{letter}', c='crimson',
    #             ha='center', fontsize=15)

    # PAA
    ax.step(object.df_PAA['t'], object.df_PAA.iloc[:, object.i_plot],
            where='post', c='royalblue', alpha=0.9)
    ax.plot([object.df_PAA['t'].iloc[-1], object.df_INT['t'].iloc[-1]],
            [object.df_PAA.iloc[-1, object.i_plot],
                object.df_PAA.iloc[-1, object.i_plot]],
            c='royalblue', alpha=0.9)

    # INT Time Series
    ax.plot(object.df_INT['t'],
            object.df_INT.iloc[:, object.i_plot], alpha=0.5)

    # Plot parameters
    ax.set_title(
        f'SAX Representation - w = {object.w}, a = {object.a}\nColumn {object.df_INT.columns[object.i_plot]}')
    ax.set_xlabel('Time')
    ax.set_xlim((object.df_INT['t'].iloc[0], object.df_INT['t'].iloc[-1]))

    plt.show()

    return


def plot_SAX(object):

    # Assign an integer to each letter (for plotting purposes)
    alphabet = np.array([chr(i)
                         for i in range(97, 97 + object.a)])[:len(object.breakpoints)+1]
    d = dict(zip([np.where(alphabet == e)[0][0]
                  for e in alphabet], alphabet))
    reverse_d = {v: k for k, v in d.items()}

    # Make some arrays to plot more easily
    sax = [reverse_d[e] for e in object.df_SAX.iloc[:, object.i_plot]]

    plt.figure(figsize=(13, 5))

    # Plot step function
    plt.step(object.df_SAX['t'], sax, where='post',
             c='k', linewidth=2, alpha=0.8)

    # Plot parameters
    plt.title(
        f'SAX Representation - w = {object.w}, a = {object.a}\nColumn {object.df_SAX.columns[object.i_plot]}')
    plt.xticks(rotation='vertical')
    plt.yticks(range(len(alphabet)), alphabet)
    plt.grid()

    plt.show()

    return
