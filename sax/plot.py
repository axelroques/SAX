
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


def plot_INT_subsequences(object):
    """
    Plots the normalization step for multiple subsequences.
    """

    selection = object.df_INT[:5]

    _, axes = plt.subplots(len(selection), 1, figsize=(13, 10))

    # Plot up to the first 5 normalized subsequences of the time series
    for i, (df, ax) in enumerate(zip(selection, axes.ravel())):
        ax.plot(df['t'], df.iloc[:, object.i_plot])
        ax.set_title(
            f'Inverse Normal Transformation - Column {df.columns[object.i_plot]}\nSubsequence {i}')
        ax.set_xlabel('Time')

    plt.tight_layout()
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


def plot_PAA_subsequences(object):
    """
    Plots the PAA representation for multiple subsequences.
    """

    selection_INT = object.df_INT[:5]
    selection_PAA = object.df_PAA[:5]

    _, axes = plt.subplots(len(selection_INT), 1, figsize=(13, 15))

    # Plot up to the first 5 PAA subsequences of the time series
    for i, (df_INT, df_PAA, ax) in enumerate(zip(selection_INT, selection_PAA, axes.ravel())):

        for line in object.breakpoints:
            ax.axhline(line, c='crimson', alpha=0.4, ls='--', lw=0.7)

        # PAA
        ax.step(df_PAA['t'], df_PAA.iloc[:, object.i_plot],
                where='post', c='royalblue', alpha=0.9)
        ax.plot([df_PAA['t'].iloc[-1], df_INT['t'].iloc[-1]],
                [df_PAA.iloc[-1, object.i_plot],
                    df_PAA.iloc[-1, object.i_plot]],
                c='royalblue', alpha=0.9)

        # INT Time Series
        ax.plot(df_INT['t'],
                df_INT.iloc[:, object.i_plot], alpha=0.5)

        # Plot parameters
        ax.set_title(
            f'SAX Representation - w = {object.w}, a = {object.a}\nColumn {df_INT.columns[object.i_plot]} - Subsequence {i}')
        ax.set_xlabel('Time')
        ax.set_xlim((df_INT['t'].iloc[0], df_INT['t'].iloc[-1]))

    plt.tight_layout()
    plt.show()

    return


def plot_SAX(object):
    """
    Plots the SAX representation.
    """

    _, ax = plt.subplots(figsize=(13, 5))

    alphabet = object.alphabet

    if object.alphabet_type == 'letters':

        # Assign an integer to each letter (for plotting purposes)
        d = dict(zip([np.where(alphabet == e)[0][0]
                      for e in alphabet], alphabet))
        reverse_d = {v: k for k, v in d.items()}

        sax = [reverse_d[e] for e in object.df_SAX.iloc[:, object.i_plot]]

    else:
        sax = object.df_SAX.iloc[:, object.i_plot].to_list()

    # Plot step function
    ax.step(object.df_SAX['t'], sax, where='post',
            c='k', linewidth=2, alpha=0.8)
    # Plot final point
    ax.plot([object.df_SAX['t'].iloc[-1], object.df_INT['t'].iloc[-1]],
            [sax[-1], sax[-1]],
            c='k', linewidth=2, alpha=0.8)

    # Plot parameters
    ax.set_title(
        f'SAX Representation - w = {object.w}, a = {object.a}\nColumn {object.df_SAX.columns[object.i_plot]}')
    plt.xticks(rotation='vertical')

    if object.alphabet_type == 'letters':
        plt.yticks(range(len(alphabet)), alphabet)
    else:
        plt.yticks(np.arange(np.min(alphabet),
                             np.max(alphabet)+1),
                   alphabet)
    plt.grid()

    plt.show()

    return


def plot_SAX_subsequences(object):
    """
    Plots the SAX representation for multiple subsequences.
    """

    selection_INT = object.df_INT[:5]
    selection_SAX = object.df_SAX[:5]

    _, axes = plt.subplots(len(selection_SAX), 1, figsize=(13, 15))

    alphabet = object.alphabet

    if object.alphabet_type == 'letters':

        # Assign an integer to each letter (for plotting purposes)
        d = dict(zip([np.where(alphabet == e)[0][0]
                      for e in alphabet], alphabet))
        reverse_d = {v: k for k, v in d.items()}

    # Plot up to the first 5 PAA subsequences of the time series
    for i, (df_INT, df_SAX, ax) in enumerate(zip(selection_INT, selection_SAX, axes.ravel())):

        if object.alphabet_type == 'letters':
            sax = [reverse_d[e] for e in df_SAX.iloc[:, object.i_plot]]

        else:
            sax = df_SAX.iloc[:, object.i_plot].to_list()

        # Plot step function
        ax.step(df_SAX['t'], sax, where='post',
                c='k', linewidth=2, alpha=0.8)
        # Plot final point
        ax.plot([df_SAX['t'].iloc[-1], df_INT['t'].iloc[-1]],
                [sax[-1], sax[-1]],
                c='k', linewidth=2, alpha=0.8)

        # Plot parameters
        ax.set_title(
            f'SAX Representation - w = {object.w}, a = {object.a}\nColumn {df_SAX.columns[object.i_plot]} - Subsequence {i}')
        ax.tick_params(axis="x", rotation=90)

        if object.alphabet_type == 'letters':
            ax.set_yticks(range(len(alphabet)))
            ax.set_yticklabels(alphabet)
        else:
            ax.set_yticks(np.arange(np.min(alphabet),
                                    np.max(alphabet)+1))
            ax.set_yticklabels(alphabet)

        ax.grid()

    plt.tight_layout()
    plt.show()

    return
