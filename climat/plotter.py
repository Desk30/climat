import matplotlib.pyplot as plt


def plot(data, **kwargs):
    fig, ax = plt.subplots()
    data.plot(**kwargs)
    plt.show()
    return fig
