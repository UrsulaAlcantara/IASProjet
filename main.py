from preprocessing import Preprocessing1
from model import Model1, Model2, Model3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold


def bootstrapped_error(func, tab, it):
    v_tab = []
    for _ in range(it):
        v_tab.append(func(np.random.choice(tab, tab.shape[0])))
    return np.array(v_tab).std()


def main():
    dataset = pd.read_csv("dataset.csv", sep=";")

    index, X, Y = Preprocessing1().get(dataset)

    X_train, X_test, Y_train, Y_test, index_train, index_test = train_test_split(
        X, Y, index, test_size=0.2, random_state=0)

    model = Model3()

    kf = KFold(n_splits=10, shuffle=True)
    cv_scores = cross_val_score(
        model, X_train, Y_train, cv=kf,  n_jobs=10, verbose=1)

    print(
        f"Score de cross validation: {cv_scores.mean()}, std: {cv_scores.std()}")

    model.fit(X_train, Y_train)
    print(f"Score de test: {model.score(X_test, Y_test)}")

    Y_test_pred = model.predict(X_test)

    error = (Y_test_pred - Y_test).abs()
    print(f"Moyenne d'erreur sur le test: {error.mean()}, std: {error.std()}")

    Y_test_sup0 = Y_test > 0
    Y_test_pred_sup0 = Y_test_pred > 0

    correct_pred = Y_test_sup0 == Y_test_pred_sup0
    print(
        f"Taux de bonne prediction pos/neg: {correct_pred.mean()}, bootstrapped err: {bootstrapped_error(np.mean, correct_pred, 10000)}")


if __name__ == "__main__":
    main()
