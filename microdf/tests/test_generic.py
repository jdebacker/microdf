from microdf.generic import MicroDataFrame
import numpy as np
import microdf as mdf


def test_df_init():
    arr = np.array([0, 1, 1])
    w = np.array([3, 0, 9])
    df = mdf.MicroDataFrame({"a": arr}, weights=w)
    assert df.a.mean() == np.average(arr, weights=w)

    df = mdf.MicroDataFrame()
    df["a"] = arr
    df.set_weights(w)
    assert df.a.mean() == np.average(arr, weights=w)

    df = mdf.MicroDataFrame()
    df["a"] = arr
    df["w"] = w
    df.set_weight_col("w")
    assert df.a.mean() == np.average(arr, weights=w)


def test_series_getitem():
    arr = np.array([0, 1, 1])
    w = np.array([3, 0, 9])
    s = mdf.MicroSeries(arr, weights=w)
    assert s[[1, 2]].sum() == np.sum(arr[[1, 2]] * w[[1, 2]])

    assert s[1:3].sum() == np.sum(arr[1:3] * w[1:3])


def test_sum():
    arr = np.array([0, 1, 1])
    w = np.array([3, 0, 9])
    series = mdf.MicroSeries(arr, weights=w)
    assert series.sum() == (arr * w).sum()

    arr = np.linspace(-20, 100, 100)
    w = np.linspace(1, 3, 100)
    series = mdf.MicroSeries(arr)
    series.set_weights(w)
    assert series.sum() == (arr * w).sum()

    # Verify that an error is thrown when passing weights of different size
    # from the values.
    w = np.linspace(1, 3, 101)
    series = mdf.MicroSeries(arr)
    try:
        series.set_weights(w)
        assert False
    except Exception:
        pass


def test_mean():
    arr = np.array([3, 0, 2])
    w = np.array([4, 1, 1])
    series = mdf.MicroSeries(arr, weights=w)
    assert series.mean() == np.average(arr, weights=w)

    arr = np.linspace(-20, 100, 100)
    w = np.linspace(1, 3, 100)
    series = mdf.MicroSeries(arr)
    series.set_weights(w)
    assert series.mean() == np.average(arr, weights=w)

    w = np.linspace(1, 3, 101)
    series = mdf.MicroSeries(arr)
    try:
        series.set_weights(w)
        assert False
    except Exception:
        pass


def test_poverty_count():
    arr = np.array([10000, 20000, 50000])
    w = np.array([1123, 1144, 2211])
    df = MicroDataFrame(weights=w)
    df["income"] = arr
    df["threshold"] = 16000
    assert df.poverty_count("income", "threshold") == w[0]


def test_median():
    # 1, 2, 3, 4, *4*, 4, 5, 5, 5
    arr = np.array([1, 2, 3, 4, 5])
    w = np.array([1, 1, 1, 3, 3])
    series = mdf.MicroSeries(arr, weights=w)
    assert series.median() == 4


def test_unweighted_groupby():
    df = mdf.MicroDataFrame({"x": [1, 2], "y": [3, 4], "z": [5, 6]})
    assert (df.groupby("x").z.sum().values == np.array([5.0, 6.0])).all()


def test_multiple_groupby():
    df = mdf.MicroDataFrame({"x": [1, 2], "y": [3, 4], "z": [5, 6]})
    assert (df.groupby(["x", "y"]).z.sum() == np.array([5, 6])).all()