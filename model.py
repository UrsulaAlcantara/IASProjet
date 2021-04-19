from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.neural_network import MLPRegressor


class Model1(BayesianRidge):
    def __init__(self):
        super().__init__(alpha_1=1e-07, alpha_2=0.01, n_iter=30)


class Model2(LinearRegression):
    def __init__(self):
        super().__init__(fit_intercept=True)


class Model3(MLPRegressor):
    def __init__(self):
        super().__init__(activation="logistic", hidden_layer_sizes=(
            100, 50, 30, 20), max_iter=150, random_state=0)


def main():
    Model1()
    Model2()
    Model3()


if __name__ == "__main__":
    main()
