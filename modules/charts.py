import upsetplot
from matplotlib import pyplot


def write_upset_chart(datasets, outpath):
    print(datasets.keys())
    df = upsetplot.from_contents(datasets)
    print(df)
    upsetplot.plot(df)
    pyplot.savefig(outpath)
