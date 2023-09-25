import seaborn as sns


def plot_hist(col, bins=30, title="", xlabel="", ax=None):
    sns.distplot(col, bins=bins, ax=ax)
    ax.set_title(f'Histogram of {title}', fontsize=20)
    ax.set_xlabel(xlabel)
